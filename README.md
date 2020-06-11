# Rasperry Pi Barcode Scanner for Kolonial.no API

Are you tired of forgetting to order new milk when it is empty?

Now you can scan the empty carton before you recycle it, and a new one will be automatically added to your cart! 😃

## Hardware
#### Tested with
- Raspberry Pi 4 Model B 4GB
- Raspberry Pi HQ Camera w/ 6mm Wide Angle Lens

## Installation
Using **Python >= 3.6**:

```shell
$ pip install -r requirements.txt
$ pip install git+https://github.com/frefrik/python-kolonial.git
$ sudo usermod -a -G video $(whoami)
```

## Usage
Edit your API credentials in `scanner.py`
```python
USERNAME = 'your@email'
PASSWORD = 'yourPassword'
USER_AGENT = 'yourUserAgent'
TOKEN = 'yourToken'
```

Start the scanner
```shell
$ python scanner.py
```

### Example output
```shell
raspberrypi:~/kolonial-barcode-scanner $ python scanner.py
Starting video stream...
Video stream started

----------------------------------------
Found product: Nidar New Energy 45 g
DING! Product added to cart :D
----------------------------------------
```
