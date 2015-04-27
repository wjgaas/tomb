FROM tomb/ubuntu:base

VOLUME ["/home/dirlt/repo"]
VOLUME ["/home/dirlt/KuaiPan"]
EXPOSE 80
EXPOSE 22

USER dirlt
RUN touch .vmflag
USER root

RUN apt-get install -y zsh
RUN chsh -s /bin/zsh dirlt

CMD /usr/sbin/sshd -D
