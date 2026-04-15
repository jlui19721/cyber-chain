# cyber-chain
This is a raspberry pi project that creates an emoji animation that users would be able to interact with on the LCD display.

# H/W Components
* Raspberry Pi
   * Raspberry Pi 4B (used for development)
   * Raspberry Pi Zero 2 W (for production)
* Pimoroni [Pirate Audio board](https://shop.pimoroni.com/products/pirate-audio-mini-speaker?variant=31189753692243)
   * Pirate Audio S/W ([here](https://github.com/pimoroni/pirate-audio))
   * Includes:
       * 1.3" IPS colour LCD (240x240px) ([ST7789 driver](https://github.com/pimoroni/st7789-python))
       * Four tactile buttons
       * Mini speaker (1W / 8Ω, attached)
* Microphone (TBD)
* UPS + voltage regulator (TBD)

# Manual Build
```
git clone ``
git submodule update --init --recursive

python3 -m venv venv
source venv/bin/activate

pip install Pillow
pip install ./third-party/st7789-python
pip install RPi.GPIO
```
# Create virtual environment with `
