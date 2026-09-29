# ============================================================
# update.R  --  IST2083 ders materyallerini günceller
# Kullanım: IST2083.Rproj dosyasını RStudio'da açın, sonra
#           Console'a şunu yazın:   source("update.R")
# ============================================================

local({
  branch <- "main"
  remote <- paste0("origin/", branch)
  
  if (!dir.exists(".git")) {
    stop("Bu dosya proje klasöründe çalıştırılmalı. ",
         "Önce IST2083.Rproj dosyasını açın (File > Open Project).", call. = FALSE)
  }
  
  # git komutu: çıktıyı ve hata durumunu döndürür (Türkçe dosya adları için quotepath kapalı)
  git <- function(...) {
    out <- suppressWarnings(system2("git", c("-c", "core.quotepath=off", ...),
                                    stdout = TRUE, stderr = TRUE))
    status <- attr(out, "status")
    list(out = enc2native(as.character(out)), ok = is.null(status) || status == 0)
  }
  ident <- c("-c", "user.name=ogrenci", "-c", "user.email=ogrenci@localhost")
  
  # Bu depoya yükleme (push) yapılamaz; yanlışlıkla denenirse net hata versin
  git("remote", "set-url", "--push", "origin", "DISABLED")
  
  # 1) Güncellemeleri indir
  fetched <- git("fetch", "origin")
  if (!fetched$ok) {
    stop("Güncellemeler indirilemedi. İnternet bağlantınızı kontrol edin.\n",
         paste(fetched$out, collapse = "\n"), call. = FALSE)
  }
  
  # 2) Öğrencinin değiştirdiği izlenen (tracked) dosyaları bul
  base <- git("merge-base", "HEAD", remote)
  mine <- character(0)
  if (base$ok && length(base$out) == 1) {
    d <- git("diff", "--name-only", base$out)
    if (d$ok) mine <- d$out[nzchar(d$out)]
  }
  changed <- mine[file.exists(mine)]
  
  # 3) Yedekle: dosya kopyaları + (güvenlik ağı olarak) yerel bir yedek dalı
  if (length(mine) > 0) {
    stamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
    dest  <- file.path("my_work", paste0("yedek_", stamp))
    
    for (f in changed) {
      dir.create(file.path(dest, dirname(f)), recursive = TRUE, showWarnings = FALSE)
      file.copy(f, file.path(dest, f), overwrite = TRUE)
    }
    
    snap <- git(ident, "stash", "create")
    snap_ref <- if (snap$ok && length(snap$out) == 1 && nzchar(snap$out)) snap$out else "HEAD"
    git("branch", paste0("yedek_", stamp), snap_ref)
    
    if (length(changed) > 0) {
      message("Değiştirdiğiniz dosyalar yedeklendi: ", dest)
      message("  - ", paste(changed, collapse = "\n  - "))
    }
  }
  
  # 4) Yerel klasörü ders deposuyla eşitle (my_work/ ve izlenmeyen dosyalar dokunulmaz)
  reset <- git("reset", "--hard", remote)
  if (!reset$ok) {
    stop("Güncelleme uygulanamadı:\n", paste(reset$out, collapse = "\n"), call. = FALSE)
  }
  message("Materyaller güncellendi. Başarılı.")
  invisible(TRUE)
})