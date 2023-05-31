What is shrike
==============

Shrike is a small and simple tool that creates JPEG File Interchange Format (JFIF) + JavaScript polyglots.

How to use it
=============

Shrike takes two arguments, path to `.jpg` file and path to `.js` file. JPG file has to be JFIF. JavaScript file can contain any JS code and has to weigh less than 64 KB.

Usage with example files:
```
python3 shrike.py shrike.jpg payload.js
```
Above command will generate `polyglot_shrike.jpg` that can be now used. 

How to exploit
==============

Due to first four bytes `0xFFD8FFE0` that are non-ASCII characters when interpreted as a text file, a character set needs to be changed to ISO/IEC 8859-1. If running in `<script>` tag, this can be achieved by adding `charset="ISO-8859-1"` inside it:

```
<script charset="ISO-8859-1" src=polyglot_shrike></script>
```

The polyglot file cannot be used with its `.jpg` extension inside a `<script>` tag. This could be done in Firefox until some time but it's fixed now.