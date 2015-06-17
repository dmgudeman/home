imap ii <Esc>
set nu

set textwidth=80
set colorcolumn=+1
set ruler

set nocompatible
filetype off

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required! 
Bundle 'gmarik/vundle'

" The bundles you install will be listed here

filetype plugin indent on

" The rest of your config follows here
augroup vimrc_autocmds

autocmd!
" highlight characters past column 120
autocmd FileType python highlight Excess ctermbg=DarkGrey guibg=White
autocmd FileType python match Excess /\%80v.*/
autocmd FileType python set nowrap
augroup END
