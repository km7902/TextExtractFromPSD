import csv
import os

from decimal import Decimal, ROUND_HALF_UP
from psd_tools import PSDImage

# Output
out_data = ''
out_path = '%s/%s' % (os.getcwd(), 'TextExtractFromPSD.txt')
csv_data = [['Text', 'Aux', 'Font', 'Size', 'HEX', 'A', 'R', 'G', 'B', 'FontWeight', 'FontStyle', 'TextDecoration']]
csv_path = '%s/%s' % (os.getcwd(), 'TextExtractFromPSD.csv')


# Add to CSS pool
def add_style(layer_name, style_dict):

    # If it default value, won't be output
    code  = '\n.%s {\n' % layer_name
    code += '    color: %s;\n' % style_dict['color']
    code += '    font-family: %s;\n' % style_dict['font-family']
    code += '    font-size: %s;\n' % style_dict['font-size']
    if not 'normal' in style_dict['font-style']:
        code += '    font-style: %s;\n' % style_dict['font-style']
    if not 'normal' in style_dict['font-weight']:
        code += '    font-weight: %s;\n' % style_dict['font-weight']
    if not 'none' in style_dict['text-decoration']:
        code += '    text-decoration: %s;\n' % style_dict['text-decoration']
    code += '}\n'
    return code


# Add to CSV
def csv_style(pool_text, css_id, aux_id):
    global csv_data

    # Do nothing if text is empty
    if pool_text == '':
        return

    csv_data.append([
        pool_text.replace('\r', '<br>'),
        aux_id,
        str(css[css_id]['font-family']).replace('\'', ''),
        css[css_id]['font-size'],
        '#%s%s%s' % (
            format(css[css_id]['color_r'], '02x'),
            format(css[css_id]['color_g'], '02x'),
            format(css[css_id]['color_b'], '02x')
        ),
        css[css_id]['color_a'],
        css[css_id]['color_r'],
        css[css_id]['color_g'],
        css[css_id]['color_b'],
        css[css_id]['font-weight'],
        css[css_id]['font-style'],
        css[css_id]['text-decoration']
    ])


# Normalizes the number 'f' after the decimal point and returns it as a string
def decimal_normalize(f):
    def _remove_exponent(d):
        return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
    a = Decimal.normalize(Decimal(str(f)))
    b = _remove_exponent(a)
    return str(b)


# Entry point

# Specify PSD file
target = input('Target PSD file path: ').strip()

# Exit if file not specified or doesn't exist
if target == '' or not os.path.exists(target):
    exit()

# Open PSD file
psd = PSDImage.open(target)


# For each layer
for layer in list(psd.descendants()):

    # If type layer
    if layer.kind == 'type':

        # Get current layer name
        layer_name = layer.name

        # Get current layer text
        layer_text = layer.text

        # Create style dictionary
        css = {}
        css_id = 0

        # Create current layer fontset list
        fontset_array = []

        # Get current layer fontset list
        for FontSet in layer.resource_dict['FontSet']:
            fontset_array.append(FontSet['Name'])

        # Get style of string
        for RunArray in layer.engine_dict['StyleRun']['RunArray']:

            # Add to style dictionary
            css[css_id] = {}

            # Extract StyleSheetData
            StyleSheetData = RunArray['StyleSheet']['StyleSheetData']

            # Typeface
            css[css_id]['font-family'] = fontset_array[StyleSheetData['Font']]

            # Font size (If the type layer is deformed, it will be reflected in font size)
            transform_yy = 1.0 if layer.transform[3] == 0.0 else layer.transform[3]
            css[css_id]['font-size'] = str(decimal_normalize(round(StyleSheetData['FontSize'] * transform_yy, 2))) + 'px'

            # Font style (Italic)
            if 'FauxItalic' in StyleSheetData:
                css[css_id]['font-style'] = 'normal' if not StyleSheetData['FauxItalic'] else 'italic'
            else:
                css[css_id]['font-style'] = 'normal'

            # Font weight (Bold)
            if 'FauxBold' in StyleSheetData:
                css[css_id]['font-weight'] = 'normal' if not StyleSheetData['FauxBold'] else 'bold'
            else:
                css[css_id]['font-weight'] = 'normal'

            # Underline
            if 'Underline' in StyleSheetData:
                css[css_id]['text-decoration'] = 'none' if not StyleSheetData['Underline'] else 'underline'
            else:
                css[css_id]['text-decoration'] = 'none'

            # Text color (ex. A:1.0 R:0.0 G:0.0 B:0.0 -> A:255 R:0 G:0 B:0)
            css[css_id]['color_a'] = StyleSheetData['FillColor']['Values'][0] * 255
            css[css_id]['color_r'] = StyleSheetData['FillColor']['Values'][1] * 255
            css[css_id]['color_g'] = StyleSheetData['FillColor']['Values'][2] * 255
            css[css_id]['color_b'] = StyleSheetData['FillColor']['Values'][3] * 255
            css[css_id]['color_a'] = int(Decimal(css[css_id]['color_a']).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
            css[css_id]['color_r'] = int(Decimal(css[css_id]['color_r']).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
            css[css_id]['color_g'] = int(Decimal(css[css_id]['color_g']).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
            css[css_id]['color_b'] = int(Decimal(css[css_id]['color_b']).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

            # Hex if text color is opaque (ex. #FFFFFF)
            if css[css_id]['color_a'] == 255:
                css[css_id]['color'] = '#%s%s%s' % (
                    format(css[css_id]['color_r'], '02x'),
                    format(css[css_id]['color_g'], '02x'),
                    format(css[css_id]['color_b'], '02x'),
                )

            # Decimal if text color isn't opaque (ex. rgba(255, 255, 255, 0.9) )
            else:
                css[css_id]['color'] = 'rgba(%s, %s, %s, %s)' % (
                    css[css_id]['color_r'],
                    css[css_id]['color_g'],
                    css[css_id]['color_b'],
                    int(css[css_id]['color_a'] / 255))

            # Go to next style dictionary
            css_id += 1

        # Reset style dictionary's KEY-ID
        css_id = 0

        pool_text = ''   # Text pool
        pool_html = ''   # HTML pool
        pool_css = ''    # CSS pool

        aux_id = 1       # Auxiliary tag num
        aux_flag = False # Auxiliary tag flag

        # Generate HTML and CSS with reference to RunLength of each style
        for RunLength in layer.engine_dict['StyleRun']['RunLengthArray']:

            # The first style of the string is overall standard style
            if css_id == 0:

                # Add to CSV
                csv_style(layer_text.strip(), css_id, aux_id - 1)

                # Cut out string to length specified by RunLength
                pool_html += layer_text[0:RunLength]
                layer_text = layer_text[RunLength:]

                # Add to CSS pool
                pool_css = add_style(layer_name, css[0])

            else:

                # If different from style of previous string
                if css[css_id - 1] != css[css_id]:

                    # Define style name of auxiliary tag
                    style_name = '%s_aux%s' % (layer_name, str(aux_id))

                    # If continues auxiliary tag, then close tag
                    if aux_flag:
                        pool_html += '</span>'
                        aux_flag = False

                        # Add to CSV
                        csv_style(pool_text.strip(), css_id - 1, aux_id - 1)
                        pool_text = ''

                    # If different from style of overall standard, start a new auxiliary tag
                    if not aux_flag and css[0] != css[css_id]:
                        pool_html += '<span class="%s">' % style_name
                        aux_id += 1
                        aux_flag = True

                    # Cut out string to length specified by RunLength
                    pool_text += layer_text[0:RunLength] if aux_flag else ''
                    pool_html += layer_text[0:RunLength]
                    layer_text = layer_text[RunLength:]

                    # Add to CSS pool
                    if css[0] != css[css_id]:
                        pool_css += add_style(style_name, css[css_id])

                # If it's same as style of previous string, only cut out string
                else:

                    # Cut out string to length specified by RunLength
                    pool_text += layer_text[0:RunLength] if aux_flag else ''
                    pool_html += layer_text[0:RunLength]
                    layer_text = layer_text[RunLength:]

            # Go to next style dictionary
            css_id += 1

        # If continues auxiliary tag, then close tag (finally)
        if aux_flag:
            pool_html += '</span>'

            # Add to CSV
            csv_style(pool_text.strip(), css_id - 1, aux_id - 1)

        # Output
        out_data += '\n<p class="%s">%s</p>\n\n<style>%s\n</style>\n' % (layer_name, pool_html.replace('\r', '<br>'), pool_css.rstrip())

# Write 'txt' file
with open(out_path, mode='w', newline='') as f:
    f.write(out_data)

# Write 'csv' file
with open(csv_path, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)
