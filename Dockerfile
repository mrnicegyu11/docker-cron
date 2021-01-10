FROM ubuntu:focal
MAINTAINER Dustin.Kaiser@gmx.net

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron
# fix via https://stackoverflow.com/questions/44184661/set-dns-options-during-docker-build/48326305
RUN echo "nameserver 208.67.222.222" > /etc/resolv.conf && \ 
    echo "search opendns.com" >> /etc/resolv.conf && echo "..." &&\    
	apt-get update
RUN echo "nameserver 208.67.222.222" > /etc/resolv.conf && \ 
    echo "search opendns.com" >> /etc/resolv.conf && \    
	apt-get -y --fix-missing install imagemagick python3 vim
# Compile and install fresh ffmpeg from sources:
# See: https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
# via https://stackoverflow.com/questions/53944487/how-to-install-ffmpeg-in-a-docker-container
# Run the command on container startup
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin
RUN echo "nameserver 208.67.222.222" > /etc/resolv.conf && \ 
    echo "search opendns.com" >> /etc/resolv.conf && \    
	apt-get -y install tzdata
RUN echo "nameserver 208.67.222.222" > /etc/resolv.conf && \ 
    echo "search opendns.com" >> /etc/resolv.conf && \    
	apt-get update -qq && apt-get -y install \
      autoconf \
      automake \
      build-essential \
      cmake \
      git-core \
      libass-dev \
      libfreetype6-dev \
      libsdl2-dev \
      libtool \
      libva-dev \
      libvdpau-dev \
      libvorbis-dev \
      libxcb1-dev \
      libxcb-shm0-dev \
      libxcb-xfixes0-dev \
      pkg-config \
      texinfo \
      wget \
      zlib1g-dev \
      nasm \
      yasm \
      libx265-dev \
      libnuma-dev \
      libvpx-dev \
      libmp3lame-dev \
      libopus-dev \
      libx264-dev \
      libfdk-aac-dev
RUN echo "nameserver 208.67.222.222" > /etc/resolv.conf && \ 
    echo "search opendns.com" >> /etc/resolv.conf && \    
	mkdir -p ~/ffmpeg_sources ~/bin && cd ~/ffmpeg_sources && \
    wget -O ffmpeg-4.3.1.tar.bz2 https://ffmpeg.org/releases/ffmpeg-4.3.1.tar.bz2 && \
    tar xjvf ffmpeg-4.3.1.tar.bz2 && \
    cd ffmpeg-4.3.1 && \
    PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
      --prefix="$HOME/ffmpeg_build" \
      --pkg-config-flags="--static" \
      --extra-cflags="-I$HOME/ffmpeg_build/include" \
      --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
      --extra-libs="-lpthread -lm" \
      --bindir="$HOME/bin" \
      --enable-libfdk-aac \
      --enable-gpl \
      --enable-libass \
      --enable-libfreetype \
      --enable-libmp3lame \
      --enable-libopus \
      --enable-libvorbis \
      --enable-libvpx \
      --enable-libx264 \
      --enable-libx265 \
      --enable-nonfree && \
    PATH="$HOME/bin:$PATH" make -j8 && \
    make install -j8 && \
    hash -r
RUN mv ~/bin/ffmpeg /usr/local/bin && mv ~/bin/ffprobe /usr/local/bin && mv ~/bin/ffplay /usr/local/bin
RUN echo "nameserver 208.67.222.222" > /etc/resolv.conf && \ 
    echo "search opendns.com" >> /etc/resolv.conf && \    
	apt-get -y install cron

CMD cron && tail -f /var/log/cron.log


