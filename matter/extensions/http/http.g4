grammar http;


http_message: start_line (header_field CRLF)* CRLF;


start_line: request_line;

request_line: method SP request_target SP http_version CRLF;


method: 'GET'| 'HEAD' | 'POST' | 'PUT' | 'DELETE' | 'CONNECT'| 'OPTIONS' | 'TRACE';


request_target: origin_form;


origin_form: absolute_path (QuestionMark query)?;

absolute_path: ( Slash segment )+;

segment: pchar+;

query: (pchar | Slash | QuestionMark)*;

http_version: http_name DIGIT Dot DIGIT;

http_name: 'HTTP/';

header_field: field_name Colon OWS* field_value OWS*;

/*
 field-name = token
 */
field_name: token;

/*
 token
 */
token: tchar+;
/*
 field-value = ( field-content / obs-fold )
 */
field_value: (field_content | obs_fold)+;

/*
 field-content = field-vchar [ 1*( SP / HTAB )  field-vchar ]
 */
field_content: field_vchar ((SP | HTAB)+ field_vchar)?;

/*
 field-vchar = VCHAR / obs-text
 */
field_vchar: vCHAR | obs_text;
/*
 obs-text = %x80-FF
 */
obs_text: OBS_TEXT;
/*
 obs-fold = CRLF  1*( SP / HTAB ) ; see RFC 7230 – Section 3.2.4
 */
obs_fold: CRLF (SP | HTAB)+;

/*
 message-body = OCTET
 */
//message_body: OCTET*;


/*
 SP = %x20 ; space
 */
SP: ' ';

pchar: unreserved | Pct_encoded | sub_delims | Colon | At;

/*
 unreserved = ALPHA /  DIGIT /  "-" /  "." /  "_" /  "~"
 */
unreserved: ALPHA | DIGIT | Minus | Dot | Underscore | Tilde;

/*
 ALPHA = %x41‑5A /  %x61‑7A ; A‑Z / a‑z
 */
ALPHA: [A-Za-z];

/*
 DIGIT = %x30‑39 ; 0-9
 */
DIGIT: [0-9];

/*
 pct-encoded = "%"  HEXDIG  HEXDIG
 */
Pct_encoded: Percent HEXDIG HEXDIG;

/*
 HEXDIG = DIGIT /  "A" /  "B" /  "C" /  "D" /  "E" /  "F"
 */
HEXDIG: DIGIT | 'A' | 'B' | 'C' | 'D' | 'E' | 'F';

/*
 sub-delims = "!" /  "$" /  "&" /  "'" /  "(" /  ")" /  "*" /  "+" /  "," /  ";" /  "="
 */
sub_delims: ExclamationMark
    | DollarSign
    | Ampersand
    | SQuote
    | LColumn
    | RColumn
    | Star
    | Plus
    | 'SEMI'
    | Period
    | Equals;

LColumn:'(';
RColumn:')';

Equals:'=';
Period:',';

/*
 CRLF = CR  LF ; Internet standard newline
 */
CRLF: '\n';

/*
 tchar = "!" /  "#" /  "$" /  "%" /  "&" /  "'" /  "*" /  "+" /  "-" /  "." /  "^" /  "_" /  "`" / 
 "|" /  "~" /  DIGIT /  ALPHA
 */
tchar: ExclamationMark
    | DollarSign
    | Hashtag
    | Percent
    | Ampersand
    | SQuote
    | Star
    | Plus
    | Minus
    | Dot
    | Caret
    | Underscore
    | BackQuote
    | VBar
    | Tilde
    | DIGIT
    | ALPHA;

Minus :'-';
Dot   : '.';
Underscore: '_';
Tilde : '~';
QuestionMark :'?';
Slash :'/';
ExclamationMark: '!';
Colon:':';
At: '@';
DollarSign:'$';
Hashtag:'#';
Ampersand:'&';
Percent:'%';
SQuote:'\'';
Star:'*';
Plus:'+';
Caret:'^';
BackQuote:'`';
VBar:'|';

/*
 OWS = ( SP / HTAB ) ; optional whitespace
 */
OWS: SP | HTAB;

/*
 HTAB = %x09 ; horizontal tab
 */
HTAB: '\t';


vCHAR: ALPHA | DIGIT | VCHAR;

VCHAR: ExclamationMark
    | '"'
    | Hashtag
    | DollarSign
    | Percent
    | Ampersand
    | SQuote
    | LColumn
    | RColumn
    | RColumn
    | Star
    | Plus
    | Period
    | Minus
    | Dot
    | Slash
    | Colon
    | 'SEMI'
    | '<'
    | Equals
    | '>'
    | QuestionMark
    | At
    | '['
    | '\\'
    | Caret
    | Underscore
    | ']'
    | BackQuote
    | '{'
    | '}'
    | VBar
    | Tilde;

OBS_TEXT: '\u0080';

/*
 OCTET = %x00-FF ; 8 bits of data
 */
//OCTET: '\u0000' .. '\u001f' | VCHAR | '\u007f' .. '\u00ff' ;
