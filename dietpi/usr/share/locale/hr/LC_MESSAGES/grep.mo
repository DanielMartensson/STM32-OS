��    t      �  �   \      �	  �   �	  �   �
  �  �    o  �   �  �  }  U  4  �  �  �  F  F  �     2     F     e  &   }     �  -   �     �  !        0     L     h  ,   }     �  .   �  '   �  (   !     J  %   j     �     �     �     �     �  *   �       �     &   �     �     �     	     %  $   =     b     t     �  �   �     Q     b     k     �     �  <   �  #   �          +     B  "   V     y     �  &   �     �     �     �     �       )         J  �   _     Y  ;   p  3   �  /   �  +      '   <   #   d      �      �      �   \   �      1!     3!  4   P!     �!  !   �!  -   �!  .   �!     #"     ?"     Z"     r"     �"     �"     �"     �"     �"     �"     #     #     ,#     4#  $   G#     l#  ,   �#  *   �#     �#     �#     �#     $     $     4$     K$  -   W$  ?   �$     �$     �$    �$  �   �&  �   �'  �  �(  �  �*  ;  �,  �  �-  Z  �/  �  =1  �  93  i  5     z6  /   �6      �6  -   �6  ,   7  ;   D7     �7  %   �7     �7  !   �7     8  +    8  (   L8  8   u8  )   �8  *   �8  #   9  ,   '9     T9     X9     [9     m9     �9  (   �9     �9  �   �9  3   r:     �:     �:     �:     ;  #   ;     B;     Y;     s;  �   �;     +<     B<  !   S<     u<     �<  L   �<  4   �<     =  5   1=  h   g=  !   �=     �=     �=  <   >     Q>     k>     �>  ,   �>     �>  -   �>      ?  @  6?     w@  6   �@  .   �@  *   �@  &   A  "   BA     eA     �A     �A     �A  Y   �A     B     !B  3   @B  (   tB  1   �B  3   �B  A   C     EC     eC     �C     �C  $   �C     �C     �C     D     'D     >D     QD     kD  
   D     �D  #   �D     �D  %   �D  3   E     9E     RE     kE     �E  !   �E     �E     �E  8   �E  P   (F     yF     �F     t       O   '   e          Z      T   J              	       X   h   R   #       U              ?       q   (   6           E   [   H   -   D                o   ^       .          I              s       i   ;   S       =   m             d   f             G   0   _               n   &       )   k      *   3   N       r       %   `      j   $   @   C   
           Q   >   \   a   /   L       "             +       <   7      5       M      K      B   Y      1   4              g      p      !       :       l             b           V   W   2   9          A   F      ]   ,   P       8   c        
Context control:
  -B, --before-context=NUM  print NUM lines of leading context
  -A, --after-context=NUM   print NUM lines of trailing context
  -C, --context=NUM         print NUM lines of output context
 
Miscellaneous:
  -s, --no-messages         suppress error messages
  -v, --invert-match        select non-matching lines
  -V, --version             display version information and exit
      --help                display this help text and exit
 
Output control:
  -m, --max-count=NUM       stop after NUM selected lines
  -b, --byte-offset         print the byte offset with output lines
  -n, --line-number         print line number with output lines
      --line-buffered       flush output on every line
  -H, --with-filename       print file name with output lines
  -h, --no-filename         suppress the file name prefix on output
      --label=LABEL         use LABEL as the standard input file name prefix
       --include=GLOB        search only files that match GLOB (a file pattern)
      --exclude=GLOB        skip files that match GLOB
      --exclude-from=FILE   skip files that match any file pattern from FILE
      --exclude-dir=GLOB    skip directories that match GLOB
   -E, --extended-regexp     PATTERNS are extended regular expressions
  -F, --fixed-strings       PATTERNS are strings
  -G, --basic-regexp        PATTERNS are basic regular expressions
  -P, --perl-regexp         PATTERNS are Perl regular expressions
   -I                        equivalent to --binary-files=without-match
  -d, --directories=ACTION  how to handle directories;
                            ACTION is 'read', 'recurse', or 'skip'
  -D, --devices=ACTION      how to handle devices, FIFOs and sockets;
                            ACTION is 'read' or 'skip'
  -r, --recursive           like --directories=recurse
  -R, --dereference-recursive  likewise, but follow all symlinks
   -L, --files-without-match  print only names of FILEs with no selected lines
  -l, --files-with-matches  print only names of FILEs with selected lines
  -c, --count               print only a count of selected lines per FILE
  -T, --initial-tab         make tabs line up (if needed)
  -Z, --null                print 0 byte after FILE name
   -NUM                      same as --context=NUM
      --group-separator=SEP  print SEP on line between matches with context
      --no-group-separator  do not print separator for matches with context
      --color[=WHEN],
      --colour[=WHEN]       use markers to highlight the matching strings;
                            WHEN is 'always', 'never', or 'auto'
  -U, --binary              do not strip CR characters at EOL (MSDOS/Windows)

   -e, --regexp=PATTERNS     use PATTERNS for matching
  -f, --file=FILE           take PATTERNS from FILE
  -i, --ignore-case         ignore case distinctions in patterns and data
      --no-ignore-case      do not ignore case distinctions (default)
  -w, --word-regexp         match only whole words
  -x, --line-regexp         match only whole lines
  -z, --null-data           a data line ends in 0 byte, not newline
   -o, --only-matching       show only nonempty parts of lines that match
  -q, --quiet, --silent     suppress all normal output
      --binary-files=TYPE   assume that binary files are TYPE;
                            TYPE is 'binary', 'text', or 'without-match'
  -a, --text                equivalent to --binary-files=text
 %s home page: <%s>
 %s: PCRE detected recurse loop %s: binary file matches %s: exceeded PCRE's backtracking limit %s: exceeded PCRE's heap limit %s: exceeded PCRE's nested backtracking limit %s: exhausted PCRE JIT stack %s: input file is also the output %s: internal PCRE error: %d %s: invalid option -- '%c'
 %s: memory exhausted %s: option '%s%s' doesn't allow an argument
 %s: option '%s%s' is ambiguous
 %s: option '%s%s' is ambiguous; possibilities: %s: option '%s%s' requires an argument
 %s: option requires an argument -- '%c'
 %s: unrecognized option '%s%s'
 %s: warning: recursive directory loop ' (C) (standard input) * at start of expression + at start of expression -P supports only unibyte and UTF-8 locales ? at start of expression Example: %s -i 'hello world' menu.h main.c
PATTERNS can contain multiple patterns separated by newlines.

Pattern selection and interpretation:
 General help using GNU software: <%s>
 Invalid back reference Invalid character class name Invalid collation character Invalid content of \{\} Invalid preceding regular expression Invalid range end Invalid regular expression JIT internal error: %d License GPLv3+: GNU GPL version 3 or later <%s>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
 Memory exhausted No match No previous regular expression Packaged by %s
 Packaged by %s (%s)
 Perl matching not supported in a --disable-perl-regexp build Premature end of regular expression Regular expression too big Report %s bugs to: %s
 Report bugs to: %s
 Search for PATTERNS in each FILE.
 Success Trailing backslash Try '%s --help' for more information.
 Unknown system error Unmatched ( or \( Unmatched ) or \) Unmatched [, [^, [:, [., or [= Unmatched \{ Usage: %s [OPTION]... PATTERNS [FILE]...
 Valid arguments are: When FILE is '-', read standard input.  With no FILE, read '.' if
recursive, '-' otherwise.  With fewer than two FILEs, assume -h.
Exit status is 0 if any line is selected, 1 otherwise;
if any error occurs and -q is not given, the exit status is 2.
 Written by %s and %s.
 Written by %s, %s, %s,
%s, %s, %s, %s,
%s, %s, and others.
 Written by %s, %s, %s,
%s, %s, %s, %s,
%s, and %s.
 Written by %s, %s, %s,
%s, %s, %s, %s,
and %s.
 Written by %s, %s, %s,
%s, %s, %s, and %s.
 Written by %s, %s, %s,
%s, %s, and %s.
 Written by %s, %s, %s,
%s, and %s.
 Written by %s, %s, %s,
and %s.
 Written by %s, %s, and %s.
 Written by %s.
 Written by Mike Haertel and others; see
<https://git.sv.gnu.org/cgit/grep.git/tree/AUTHORS>. ` ambiguous argument %s for %s character class syntax is [[:space:]], not [:space:] conflicting matchers specified exceeded PCRE's line length limit failed to return to initial working directory failed to set file descriptor text/binary mode input is too large to count invalid argument %s for %s invalid character class invalid content of \{\} invalid context length argument invalid matcher %s invalid max count memory exhausted no syntax specified program error regular expression too big stack overflow stray \ stray \ before %lc stray \ before unprintable character stray \ before white space the -P option only supports a single pattern unable to record current working directory unbalanced ( unbalanced ) unbalanced [ unfinished \ escape unknown binary-files type unknown devices method warning: %s warning: --unix-byte-offsets (-u) is obsolete warning: GREP_COLOR='%s' is deprecated; use GREP_COLORS='mt=%s' write error {...} at start of expression Project-Id-Version: grep-3.7.98
Report-Msgid-Bugs-To: bug-grep@gnu.org
PO-Revision-Date: 2022-07-09 07:27+0200
Last-Translator: Božidar Putanec <bozidarp@yahoo.com>
Language-Team: Croatian <lokalizacija@linux.hr>
Language: hr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
X-Bugs: Report translation errors to the Language-Team address.
X-Generator: Poedit 3.1.1
 
Kontrola konteksta:
  -B, --before-context=BROJ  ispiše BROJ redaka konteksta koji prethode
  -A, --after-context=BROJ  ispiše BROJ redaka konteksta koji slijede
  -C, --context=BROJ        ispiše BROJ redaka konteksta koji prethode/slijede
 
Razno:
  -s, --no-messages         izostavi poruke o greškama
  -v, --invert-match        odabere redove koji se ne podudaraju
  -V, --version             informacije o inačici ovog programa
      --help                ova pomoć
 
Kontrola izlaza:
  -m, --max-count=BROJ      prestane nakon BROJ nađenih redaka
  -b, --byte-offset         uz retke ispiše i poziciju u bajtovima
  -n, --line-number         uz retke ispiše broj retka
      --line-buffered       izravno ispiše svaki izlazni redak
  -H, --with-filename       uz retke ispiše ime datoteke za svako podudaranje
  -h, --no-filename         bez ispisa imena datoteke za svako podudaranje
      --label=OZNAKA        rabi OZNAKU kao ime datoteke na standardnom ulazu
       --include=GLOB        pretraži samo datoteke koje se podudaraju
                              s GLOB-om (datoteka s uzorcima)
      --exclude=GLOB        preskoči sve datoteke i direktorije koji se
                              podudaraju s GLOB-om (datoteka s uzorcima)
      --exclude-from=DATOTEKA  preskoči sve datoteke koje se podudaraju s
                                 bilo kojim uzorkom u DATOTEKA
      --exclude-dir=GLOB    preskoči direktorije koji podudaraju GLOB
   -E, --extended-regexp     UZORAK je prošireni regularni izraz (ERE)
  -F, --fixed-strings       UZORAK je skup stringova odvojenih
                              znakom novog retka (\n)
  -G, --basic-regexp        UZORAK je osnovni regularni izraz (BRE)
  -P, --perl-regexp         UZORAK je Perl regularni izraz
   -I                        isto kao --binary-files=without-match
  -d, --directories=AKCIJA  kako rukovati direktorijima;
                              AKCIJA je „read“, „recurse“ ili „skip“
  -D, --devices=AKCIJA      kako rukovati uređajima, FIFO uređajima
                              i utičnicama;  AKCIJA je „read“ ili „skip“
  -r, --recursive           isto kao --directories=recurse
  -R, --dereference-recursive  jednako, ali slijedi svaku simboličku vezu
   -L, --files-without-match  ispiše samo imena DATOTEKA bez podudaranja
  -l, --files-with-matches  ispiše samo imena DATOTEKA s podudaranjima
  -c, --count               ispiše samo broj podudarnih redaka po DATOTECI
  -T, --initial-tab         poravna tabove (ako je potrebno)
  -Z, --null                ispiše 0-bajt nakon imena DATOTEKE
   -BROJ                     isto kao --context=BROJ
      --group-separator=SEP  ispiše SEP(arator) u retku između
                               podudaranja s kontekstom
      --no-group-separator  ne ispiše separator za podudaranja s kontektsom
      --color[=KADA],
      --colour[=KADA]       bojama istakne nađene stringove i markere;
                            KADA može biti „always“ ili „never“ ili „auto“
  -U, --binary              ne uklanja CqR znakove na EOL (MSDOS/Windows)

   -e, --regexp=UZORCI       koristi UZORKE kao regularni izraz
  -f, --file=DATOTEKA       preuzmi UZORKE iz DATOTEKE
  -i, --ignore-case         zanemari veličinu slova u uzorcima i podacima
      --no-ignore-case      ne zanemaruje veličinu slova (zadano)
  -w, --word-regexp         UZORAK podudara samo cijele riječi
  -x, --line-regexp         UZORAK podudara samo cijele redove
  -z, --null-data           redak završava s 0-bajtom, a ne sa znakom novog retka
   -o, --only-matching       prikaže samo dio retka koji se podudara
  -q, --quiet, --silent     izostavi svaki normalni izlaz (ništa ne ispiše)
      --binary-files=VRSTA  pretpostavi binarne datoteke tipa VRSTA;
                              VRSTA je „binary“, „text“ ili „without-match“
  -a, --text                isto kao --binary-files=text
 Mrežna stranica za %s: <%s>
 %s: PCRE je otkrio/naišao na rekurzivnu petlju %s: binarna datoteka se podudara %s: je premašio PCRE granicu broja pokušaja %s: je premašio PCRE granicu za hrpe (heap) %s: je premašio PCRE granicu broja ugniježdenih pokušaja %s: PCRE JIT stȏg je iscrpljen %s: ulazna datoteka je ujedno i izlaz %s: interna PCRE greška: %d %s: nevaljana opcija -- „%c“
 %s: nema dovoljno memorije %s: opcija „%s%s“ ne dopušta argument
 %s: opcija „%s%s“ nije jednoznačna
 %s: opcija „%s%s“ nije jednoznačna; mogućnosti su: %s: opcija „%s%s“ zahtijeva argument
 %s: opcija zahtijeva argument -- „%c“
 %s: neprepoznata opcija „%s%s“
 %s upozorenje: rekurzivna petlja direktorija “ © (standardni ulaz) * na početku izraza + na kraju izraza -P podržava samo unibyte i UTF-8 locale ? na početku izraza Primjer: %s -i 'hello world' menu.h main.c
UZORCI mogu sadržavati višestruke mustre odijeljene sa znakom za novi redak (\n).

Izbor uzorka i interpretacija:
 Općenita pomoć za korištenje GNU softvera: <%s>
 Nevaljana povratna referencija Nevaljano ime za klasu znakova Nevaljani znak za razvrstavanje Nevaljani sadržaj u \{\} Nevaljani prethodni regularni izraz Nevaljani kraj raspona Nevaljani regularni izraz JIT interna greška: %d Licencija GPLv3+: GNU GPL inačica 3 ili novija <%s>.
Ovo je slobodan softver: slobodno ga mijenjajte i dijelite.
NEMA JAMSTVA do granica dopuštenih zakonom.
 Nema dovoljno memorije Nema podudaranja Nema prethodnog regularnog izraza Spakirao %s
 Spakirali %s (%s)
 Kompiliranje s --disable-perl-regexp ne podržava podudaranje na Perl način Nedovršeni regularni izraz (preuranjeni završetak) Preveliki regularni izraz Pogreške %s javite (na engleskom, LC_ALL=C) na <%s>
 Greške u programu javite na <%s>.
Primjedbe i pogreške u prijevodu javite na <lokalizacija@linux.hr>.
 Traži UZORKE u svakoj DATOTECI.
 Uspjeh Zaostala obratna kosa crta Pokušajte s „%s --help“ za pomoć i više informacija.
 Nepoznata greška sustava ( ili \( nema odgovarajući par ) ili \) nema odgovarajući par [, [^, [:, [., ili [= nema odgovarajući par \{ nema odgovarajući par Uporaba: %s [OPCIJA]... UZORCI [DATOTEKA]...
 Valjani argumenti su: Ako je DATOTEKA „-“ (spojnica), čita standardni ulaz. Bez DATOTEKE,
rekurzivno čita „.“, inače čita „-“ (stdin).
S manje od dvije navedene DATOTEKE implicira opciju -h.
Završi sa statusom 0 ako je nađen barem jedan redak, inače s 1;
ako ima grešaka, a nije navedena opcija -q, završi sa statusom 2.
 Napisali %s i %s.
 Napisali %s, %s, %s,
%s, %s, %s, %s,
%s, %s i ostali.
 Napisali %s, %s, %s,
%s, %s, %s, %s,
%s i %s.
 Napisali %s, %s, %s,
%s, %s, %s, %s
i %s.
 Napisali %s, %s, %s,
%s, %s, %s i %s.
 Napisali %s, %s, %s,
%s, %s i %s.
 Napisali %s, %s, %s,
%s i %s.
 Napisali %s, %s, %s
i %s.
 Napisali %s, %s i %s.
 Napisao %s.
 Napisali Mike Haertel i ostali; vidi
<https://git.sv.gnu.org/cgit/grep.git/tree/AUTHORS>. „ višeznačni argument %s za %s sintaksa znakovne klase je [[:space]], ne [:space:] navedeni uzorci su međusobno konfliktni prekoračeno je ograničenje duljine retka PCRE-a nije se uspjelo vratiti u početni radni direktorij nije uspjelo postaviti deskriptor datoteke u tekst/binarni način ulaz je prevelik da se prebroji nevaljani argument %s za %s nevaljana znakovna klasa nevaljani sadržaj u \{\} nevaljani kontekst duljine argumenta nevaljana sintaksa uzorka %s nevaljani maksimalni broj nema dovoljno memorije sintaksa nije navedena greška u programu preveliki regularni izraz prelijevanje stȏga zalutali \ zalutali \ ispred %lc zalutali \ ispred neispisivog znaka zalutali \ ispred bijeline opcija -P podržava samo jedan uzorak nije moguće registrirati trenutni radni direktorij ( nema odgovarajući par ) nema odgovarajući par [ nema odgovarajući par nedovršena \ escape sekvencija nepoznata vrsta binarnih datoteka nepoznata metoda uređaja upozorenje: %s upozorenje: opcija--unix-byte-offsets (-u) je zastarjela upozorenje: GREP_COLOR=‘%s’ je zastarjelo; koristite GREP_COLORS=‘mt=%s’ greška pri pisanju {...} na startu izraza 