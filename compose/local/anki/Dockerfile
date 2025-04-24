FROM lsiobase/rdesktop-web:focal
# Clean up and fix broken dependencies
RUN apt-get update && apt-get install -y \
    --fix-missing \
    && apt-get install -y \
    ca-certificates \
    wget \
    python3 \
    python3-pip \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    libgl1-mesa-glx \
    libegl1-mesa \
    libgles2-mesa \
    libglib2.0-0 \
    libdbus-1-3 \
    locales \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure dpkg is in a consistent state
RUN dpkg --configure -a

VOLUME "/config/app"

COPY root/ /
