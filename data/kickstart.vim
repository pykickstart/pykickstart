" Filename:    kickstart.vim
" Purpose:     Vim syntax file
" Language:    kickstart scripting for anaconda, the Red Hat/Fedora installer
" Maintainer:  Will Woods wwoods@redhat.com
" Last Change: Thu Mar  3 11:12 EST 2016

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syntax case match 

" include other possible scripting languages people might use
let b:is_bash=1
syntax include @Shell syntax/sh.vim
unlet b:current_syntax " ha ha lies
syntax include @Python syntax/python.vim
unlet b:current_syntax " more lies
syntax include @Perl syntax/perl.vim

" comments
syntax region ksComment start=/#/ end=/$/ contains=ksTodo
syntax keyword ksTodo contained FIXME NOTE TODO NOTES XXX

" commands
syntax keyword ksCommands contained auth authconfig autopart autostep bootloader btrfs cdrom clearpart cmdline device deviceprobe displaymode dmraid driverdisk eula fcoe firewall firstboot graphical group halt harddrive ignoredisk install interactive iscsiname iscsi keyboard key lang langsupport lilocheck liveimg logging logvol mediacheck monitor mouse multipath network nfs ostreesetup part partition poweroff raid realm reboot repo reqpart rescue rootpw selinux services shutdown skipx sshkey sshpw text timezone unsupported_hardware updates upgrade url user vnc volgroup xconfig zerombr zfcp

" only match commands at the start of a new line
syntax match ksCommandLine '^\s*\l\+' contains=ksUnknownCommand nextgroup=ksCommandOpts
syntax match ksUnknownCommand contained '\l\+' contains=ksCommands
syntax match ksCommandOpts contained '.*$' contains=ksFlag
syntax match ksFlag contained '--\a[a-zA-Z0-9-]*=\?'

" includes
syntax match ksIncludes '^\s*\(%include\|%ksappend\)'

" general section start/end markers
syntax match ksSectionMarker contained '^\s*%\(addon\|anaconda\|end\|packages\|pre-install\|pre\|post\|traceback\)'

" %package section
syntax region ksPackages start=/^\s*%packages/ matchgroup=ksSectionMarker end=/^\s*%end\s*$/ contains=ksPackagesHeader,ksPackageItem,ksPackageGroup,ksComment,ksGroupFlag
syntax match ksPackagesHeader contained '^\s*%packages.*$' contains=ksSectionMarker,ksPackagesFlag
syntax match ksPackagesFlag   contained '--\(default\|excludedocs\|ignoredeps\|ignoremissing\|instLangs=\?\|nobase\|nocore\|resolvedeps\|multilib\)' 
syntax match ksPackageItem    contained '^\s*[^@#%]\S*' contains=ksPackageGlob,ksPackageMinus
syntax match ksPackageGroup   contained '^\s*@\S*' contains=ksGroupFlag
syntax match ksPackageMinus   contained '^\s*-'
syntax match ksGroupFlag      contained '--\(nodefaults\|optional\)'
syntax match ksPackageGlob    contained '\*'

" sections processed outside of pykickstart, but that it knows about
syntax region ksUnknownScript start=/^\s*%\(addon\|anaconda\)/ matchgroup=ksSectionMarker end=/^*%end\s*$/ contains=ksSectionMarker

" script sections (%pre, %post, %traceback)
syntax region ksShellScript start=/^\s*%\(pre-install\|pre\|post\|traceback\)/ matchgroup=ksSectionMarker end=/^\s*%end\s*$/ contains=@Shell,ksScriptHeader,@Shell
syntax region ksOtherScript start=/^\s*%\(pre-install\|pre\|post\|traceback\)\s.*--interpreter=.*$/ matchgroup=ksSectionMarker end=/^\s*%end\s*$/ contains=ksScriptHeader
syntax region ksPythonScript start=/^\s*%\(pre-install\|pre\|post\|traceback\)\s.*--interpreter=\S*python.*$/ matchgroup=ksSectionMarker end=/^\s*%end\s*$/ contains=@Python,ksScriptHeader
syntax region ksPerlScript start=/^\s*%\(pre-install\|pre\|post\|traceback\)\s.*--interpreter=\S*perl.*$/ matchgroup=ksSectionMarker end=/^\s*%end\s*$/ contains=@Perl,ksScriptHeader
syntax match ksScriptHeader contained '^\s*%\(pre-install\|pre\|post\|traceback\).*' contains=ksSectionMarker,ksScriptFlag
syntax match ksScriptFlag contained '--\(erroronfail\|interpreter=\?\|log=\?\|logfile=\?\|nochroot\)'

" sync to section markers
syntax sync match ksSync grouphere NONE "^\s*%\(addon\|anaconda\|end\|pre-install\|pre\|post\|packages\|traceback\)"

" Define the default highlighting.
" For version 5.7 and earlier: only when not done already
" For version 5.8 and later: only when an item doesn't have highlighting yet
if version >= 508 || !exists("did_kickstart_syntax_inits")
  if version < 508
    let did_kickstart_syntax_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif
  HiLink ksComment              Comment
  HiLink ksTodo                 Todo
  HiLink ksCommands             Statement
  HiLink ksUnknownCommand       Error
  HiLink ksIncludes             Include
  HiLink ksSectionMarker        Structure
  HiLink ksScriptFlag           ksFlag
  HiLink ksPackagesFlag         ksFlag
  HiLink ksGroupFlag            ksFlag
  HiLink ksFlag                 Identifier
  HiLink ksPackageMinus         Special
  HiLink ksPackageGroup         Include
  HiLink ksPackageGlob          Operator
  delcommand HiLink
endif

let b:current_syntax = "kickstart"

" vim: ts=8
