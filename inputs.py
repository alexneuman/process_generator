
spec_name = '221206_TRBX_jidsfjsdf'
sheet_name = 'amazon'
date, case_code, _ = spec_name.split('_')

# file_name = f'{date}_{case_code}_{sheet_name}'

input_columns = [
    'startingURL',
    'zip'
]

captures = ['numProducts', 'productName', 'regularPrice', 'salePrice']