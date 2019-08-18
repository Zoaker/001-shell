"==================================================================
"This is for vim/gvim(win7) setting
"=================================================================

syntax on             
syntax enable 
winpos 800 0                                  "set default window position
set nu                                        "set number
set lines=45 columns=110                      "set default window size
set autoindent                                "set insert space char
set backspace=indent,eol,start                

set tabstop=4                                 "Indentation levels every four coloms
set softtabstop=4                             "press tap become inserting 4 spaces, tab occupied 4 spaces
set expandtab                                 "transfer tab to space
set shiftwidth=4                              "set width of tab
set shiftround                                "Indent/outdent to neareast tabstop"
set matchpairs+=<:>                           "allow % to bounce between angles too
set nocompatible                              "use the complete function of vim
set visualbell                                "set bell to flash
set ruler                                     "show current position at the bottom
 
set hlsearch                                  "hightlight search
set ignorecase                                "ignore case sensitive
set showcmd                                   "show command
set showmode                                  "show mode
set cmdheight=2                               "command line height
set cindent 
set history=500  
