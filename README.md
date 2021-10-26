# TextExtractFromPSD

Extracts rich text from type layer of PSD (PSB) file.


## require

Require psd-tools package.

```
pip install psd-tools
```

## how to use

Execute command line.

```
python3 TextExtractFromPSD.py
```

and specify target file. (PSD or PSB)

```
Target PSD file path: /Users/username/Downloads/sample.psd
```

## OUTPUT

e.g.<br>
If you load "sample.psd"

<img src="https://github.com/km7902/TextExtractFromPSD/blob/main/sample.png" alt="">

Then 2 files will be created in the same hierarchy.

### 1. TextExtractFromPSD.txt

```
<p class="text1">H<span class="text1_aux1">A</span>P<span class="text1_aux2">P</span>Y<br>H<span class="text1_aux3">A</span>L<span class="text1_aux4">L</span>O<span class="text1_aux5">W</span>E<span class="text1_aux6">E</span>N<br></p>

<style>
.text1 {
    color: #ff9900;
    font-family: 'Arial-Black';
    font-size: 60px;
}

.text1_aux1 {
    color: #000000;
    font-family: 'Arial-Black';
    font-size: 60px;
}

.text1_aux2 {
    color: #000000;
    font-family: 'Arial-Black';
    font-size: 60px;
}

.text1_aux3 {
    color: #000000;
    font-family: 'Arial-Black';
    font-size: 60px;
}

.text1_aux4 {
    color: #000000;
    font-family: 'Arial-Black';
    font-size: 60px;
}

.text1_aux5 {
    color: #000000;
    font-family: 'Arial-Black';
    font-size: 60px;
}

.text1_aux6 {
    color: #000000;
    font-family: 'Arial-Black';
    font-size: 60px;
}
</style>
```

### 2. TextExtractFromPSD.csv

| Text | Aux | Font | Size | HEX | A | R | G | B | FontWeight | FontStyle | TextDecoration |
| ---- | --- | ---- | ---- | --- | - | - | - | - | ---------- | --------- | -------------- |
| HAPPY<br>HALLOWEEN | 0 | Arial-Black | 60px | #ff9900 | 255 | 255 | 153 | 0 | normal | normal | none |
| A | 1 | Arial-Black | 60px | #000000 | 255 | 0 | 0 | 0 | normal | normal | none |
| P | 2 | Arial-Black | 60px | #000000 | 255 | 0 | 0 | 0 | normal | normal | none |
| A | 3 | Arial-Black | 60px | #000000 | 255 | 0 | 0 | 0 | normal | normal | none |
| L | 4 | Arial-Black | 60px | #000000 | 255 | 0 | 0 | 0 | normal | normal | none |
| W | 5 | Arial-Black | 60px | #000000 | 255 | 0 | 0 | 0 | normal | normal | none |
| E | 6 | Arial-Black | 60px | #000000 | 255 | 0 | 0 | 0 | normal | normal | none |


### The MIT License (MIT)
