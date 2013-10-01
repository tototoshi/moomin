;;; moomin.el -- Edit MoinMoin with emacs

;; Copyright (C) 2013  Toshiyuki Takahashi

;; Author: Toshiyuki Takahashi (@tototoshi)
;; Keywords:

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

;;; Usage:
;;;
;;; (require 'moomin)
;;;
(require 'http-get)
(require 'helm)
(require 'screen-lines)
(require 'moinmoin-mode)

(defvar moomin-url nil)

(defvar moomin-buffer-prefix "moinmoin-")

(defun ewiki-with-emacs (title)
  (interactive "sTitle: ")
  (let ((buf (get-buffer-create
              (format "%s%s" moomin-buffer-prefix title))))
    (switch-to-buffer buf)
    (erase-buffer)
    (insert
     (print (shell-command-to-string
       (format "moomin show '%s'" title))))
    (goto-char (point-min))
    (moinmoin-mode)))

(defun moomin-file-put-contents (file-path string)
  (with-temp-buffer
    (erase-buffer)
    (insert string)
    (write-region (point-min) (point-max) file-path)))

(defun moomin-save ()
  (interactive)
  (let ((page-name (string-replace-match moomin-buffer-prefix (buffer-name) ""))
        (tmpfile "/tmp/moomin-tmpfile"))
    (moomin-file-put-contents tmpfile (buffer-substring-no-properties (point-min) (point-max)))
    (when page-name
      (shell-command-to-string
       (print (format "moomin save '%s' %s" page-name tmpfile))))
    (delete-file tmpfile)
    (message (format "save %s" page-name))))

(defun moomin-join (xs)
  (reduce '(lambda (x y) (concat x "/" y)) xs))

(defun moomin-url-encode (s)
  (moomin-join
   (mapcar '(lambda (x) (http-url-encode x 'utf-8)) (split-string s "/"))))

(defun wiki (title)
  (interactive "sTitle: ")
  (shell-command-to-string (format "moomin browse '%s'" title)))

(defun helm-moomin-page-list ()
  (split-string (shell-command-to-string "moomin list") "\r\n"))

(setq helm-c-source-moomin-page
      '((name . "Page list")
        (candidates . helm-moomin-page-list)
        (action
         . (("View" . wiki)
            ("Edit with emacs" . ewiki-with-emacs)
            ))))

(defun helm-moomin ()
  (interactive)
  (helm '(helm-c-source-moomin-page)))

(add-hook 'moinmoin-mode-hook
          (lambda ()
            (define-key moinmoin-mode-map (kbd "C-c C-c") 'moomin-save)
            (transient-mark-mode 1)))

(provide 'moomin)
