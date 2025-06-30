# LoFi-fy

Welcome to **LoFi-fy**!

## Overview

LoFi-fy is a project designed to bring lofi vibes to your development or leisure environment. Whether you want chill beats in your workspace, a music-themed web application, or a customizable audio player, LoFi-fy has you covered.

## Features
- Detects *whether a video is lofifiable* using our own fine-tuned model over 2.5k+ dataset.
- Generates music params such as (key, mode, tempo, chords(triads per measure 1), notes(per measure 8) etc. through a
[open-source model](https://lofi.jacobzhang.de/) and produces track in the browser side using *Tone.js*.
- We combine video and produced audio using *ffmpeg* alongwith multi-threading by creating separate worker.
- Create LoFi BGM videos, Arrange into playlists and Play curated lofi music streams or playlists
- Simple, clean, and user-friendly interface
- Responsive design for desktop and mobile
- Customizable themes (coming soon)
- Volume and playback controls
- Minimal distractions for maximum focus

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/TakeASwing-420/LoFi-fy.git
    cd LoFi-fy
    ```

2. **Install dependencies**
    ```bash
    # If using npm
    npm install

    # Or if using yarn
    yarn install
    ```

3. **Start the application**
    ```bash
    # If using npm
    npm start

    # Or if using yarn
    yarn start
    ```

4. **Open your browser**  
   Go to http://localhost:[port] to use LoFi-fy.

## Usage

- Navigate through the interface to play or pause lofi music.
- Adjust volume and playback settings as needed.
- Enjoy a distraction-free listening experience!

## Contributing

Contributions are welcome!  
To contribute:

1. Fork this repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the [MIT License](LICENSE).

---

Made with Love by Team Rebase @HexaFalls 2025
