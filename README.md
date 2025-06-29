# Explore Base64, Base85, Ascii85, and Z85 encoding with Python 
# Practical web app

This round of article we are going to explore a bit about how [base64][2] works, and dive into [base85][3] mechanism.  

[![b4_flowchart](/app/static/images/base85_title_img.png)](https://youtu.be/5LJTyJb2kyk)

## Quick info about how base64 works

Base64 encoding converts binary data into an ASCII string format, allowing it to be safely transported over channels that primarily handle text. It works by grouping binary data into 6-bit chunks and mapping each chunk to a corresponding character in a 64-character Base64 table. This table includes uppercase and lowercase letters, digits, and special characters like "+" and "/". 

Example:
1. Let's take 3 character from "Malaysia" as demonstration. we have the ASCII string "Mal". 
2. ASCII to Binary: "Mal" in binary is 01001101 01100001 01101100. refer to [Ascii conversion chart][1]
3. Grouping into 3 byte Chunks then split into 24-bit blocks:  


![826](/app/static/images/base64_conv_8bitsto6bits.png)

Mapping to Base64 Characters: Using the Base64 table, these 6-bit values correspond to "TWFs". 

![b64_flowchart](/app/static/images/b4_flowchart.png)

### Extras Info about padding works
- If the original binary data length is not a multiple of 3 bytes, padding is used.
- If there are 2 bytes remaining, they form a 16-bit chunk. This 16-bit chunk is treated as two 6-bit chunks, and the last 6-bit chunk is padded with two '0' bits to make it 6 bits. The output will have one = character for padding.
- If there is 1 byte remaining, it forms an 8-bit chunk. This 8-bit chunk is treated as one 6-bit chunk, and the last two 6-bit chunks are padded with '0' bits. The output will have two = characters for padding.

Padding example:  
Uses "Ma" two characters, "E" is added (padding in red color) with two '0' bits to make it 6 bits and the last 6-bit chunk is padded with '0' bits to make it 6 bits block, resulting in "TWE=". 


![b64_conv_bits](/app/static/images/base64_conv_24bits.png)

## Base64 chart
```
 0 -  9:  A B C D E F G H I J
10 - 19:  K L M N O P Q R S T
20 - 29:  U V W X Y Z a b c d
30 - 39:  e f g h i j k l m n
40 - 49:  o p q r s t u v w x
50 - 59:  y z 0 1 2 3 4 5 6 7
60 - 69:  8 9 + /
Padding =
```

Base64 is commonly used for encoding binary data in emails, storing data in XML, and including binary data in URLs. It ensures that binary data can be transmitted safely and reliably over networks that primarily handle text. 

This is a general explaination and demonstration only, more indepth and detail explaination can refer to [Base64 Wiki][2] page.

---

# How Base85 works

Similar to Base64, Base85 perform same form of binary-to-text encoding by convert binary data to printable ASCII characters and decoding back to binary data. There were 3 implementations. Base85 without Ascii, Ascii85, and ZeroMQ Base85 Encoding. Each implementation choice difference set of characters based on 94 non-whitespace printable ASCII characters.

Quote from [ZMQ RFC 32][4]

> To encode a frame, an implementation SHALL take four octets at a time from the binary frame and convert them into five printable characters. The four octets SHALL be treated as an unsigned 32-bit integer in network byte order (big endian). The five characters SHALL be output from most significant to least significant (big endian).

> To decode a string, an implementation SHALL take five characters at a time from the string and convert them into four octets of data representing a 32-bit unsigned integer in network byte order. The five characters SHALL each be converted into a value 0 to 84, and accumulated by multiplication by 85, from most to least significant.

## Base85 chart

```
 0 -  9:  0 1 2 3 4 5 6 7 8 9
10 - 19:  A B C D E F G H I J
20 - 29:  K L M N O P Q R S T
30 - 39:  U V W X Y Z a b c d
40 - 49:  e f g h i j k l m n
50 - 59:  o p q r s t u v w x
60 - 69:  y z ! # $ % & ( ) *
70 - 79:  + - ; < = > ? @ ^ _
80 - 84:  ` { | } ~
```

> Base85 chart excludes these non-whitespace printable ASCII characters "',.:[]/\

Fundamental idea of Base85 is to take a block of 4 bytes (32 bits) of binary data and represent it using 5 ASCII characters. This is more efficient than Base64, which uses 4 characters for 3 bytes.

> Ascii85 exclused these non-whitespace printable ASCII characters vwxyz{|}~

Furthermore, Ascii85 has an additional feature: it compresses 4-byte all-zero sequences to z (and optionally 4-byte all-space sequences to y) expands it by roughly 25% compare to base64 33%. This makes it particularly useful for applications where data size is a concern, such as embedding binary data in text-based formats like PostScript, PDF files, or network protocols.

### Z-Base85 Chart
```
 0 -  9:  0 1 2 3 4 5 6 7 8 9
10 - 19:  a b c d e f g h i j
20 - 29:  k l m n o p q r s t
30 - 39:  u v w x y z A B C D
40 - 49:  E F G H I J K L M N
50 - 59:  O P Q R S T U V W X
60 - 69:  Y Z . - : + = ^ ! /
70 - 79:  * ? & < > ( ) [ ] {
80 - 84:  } @ % $ #
```

> Z85 chart excludes these non-whitespace printable ASCII characters "',;_`|~\

Recently implemented in [python 3.13][5]. Z85 is a derivative of existing Ascii85 encoding mechanisms, modified for better usability, particularly for use in source code, XML, JSON, or passed on the command line. By, choose different character sets (refer to Z-Base85 Chart) to avoid characters that might have special meaning in programming languages or markup languages. This is why some variants like Z85 exist with "safer" character sets.

Generally, Z85 remain very similarity to ASCII85 implementation, takes a binary frame and encodes it as a printable ASCII string, or takes an ASCII encoded string and decodes it into a binary frame. See [ZMQ RFC 32][4] for details.

### How Z85 works in a nutshell:

1. Combine Bytes into a 32-bit Number: Take four bytes of binary data and treat them as a single 32-bit unsigned integer in big-endian order (most significant byte first).

### Mapping Example
![alt text](/app/static/images/b85_mapping.png)

2. Takes the Hex value and convert to Base10 decimal value. 

![alt text](/app/static/images/h2d.png)

### Calculation Example
![my_hex_formula](/app/static/images/t_value.png)


3. Divide this Base10 decimal value repeatedly by base 85 exponent 0 - 4, taking the remainders to the next calculation. This will yield 5 "digits" in base85 with each Quotient value (Returns the integer portion of a division)

![alt text](/app/static/images/d_value.png)

![alt text](/app/static/images/f_calc.png)

4. Map these 5 "Digits" to Z85 chart characters: Each of these 5 digits (0-84) is then mapped to a printable ASCII character.

> Z-Base85 encoding value = o<}<D

![alt text](/app/static/images/zb85_chart.png)

![mygif_demo](/app/static/images/output1.gif)

Note:
> Z-Base85 doesn't need to add 33 to each Base85 digit to get its ASCII value, because its implement diffence set of ASCII characters.


---

## Why should you consider using Z-base85 

z85 basically design to be easy to use in source code, when enclosed in double or single quotes. safer to pass on the command line, when enclosed in single quotes, and easy to implement in any programming language. In order to be the most efficient textual representation possible. It Strikes a good balance between encoding efficiency and string-safety, making it a valuable choice for developers who need to embed binary data in text-based environments while minimizing overhead and avoiding common character-related pitfalls.

i creates a simple web app tool to demonstrates how to base64 and base85 implementation encoding and decoding with Python using the `base64` module.
if you interested to explore more and try it yourself, may head over to below link to download the repo

## Installation steps

### clone repo

```html
git clone https://github.com/scheehan/encode_decode_web_app.git
cd encode_decode_web_app
```

## enable virtual env

```python
> python -m venv .venv

Linux | MacOS 
> python3 -m venv \<path\>  
> source \<path\>/bin/activate

Windows
> py -m venv \<path\>  
> \<DIR\>\Scripts\activate
```

## install dependencies

```python
> python3 -m pip install flask
```

## Run flask app

```python
> flask run --debug
```

Your app should be running at http://127.0.0.1:5000/ 


[1]: https://web.alfredstate.edu/faculty/weimandn/miscellaneous/ascii/ascii_index.html
[2]: https://en.wikipedia.org/wiki/Base64
[3]: https://en.wikipedia.org/wiki/Ascii85
[4]: https://rfc.zeromq.org/spec/32/
[5]: https://docs.python.org/3/whatsnew/3.13.html#base64



<style type="text/css">
    img {
        width: 550px;
    }
    img[alt="b4_flowchart"] {
        width: 800px;
    }
    img[alt="b64_conv_bits"] {
        width: 800px;
    }
    img[alt="826"] {
        width: 800px;
    }
    img[alt="my_hex_formula"] {
        width: 800px;
    }
    img[alt="mygif_demo"] {
        width: 700px;
    }
    
</style>
