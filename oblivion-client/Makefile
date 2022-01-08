OBLIVION=target/oblivion.exe

all: $(OBLIVION)

$(OBLIVION): src/oblivion.py
	cxfreeze src/oblivion.py --target-dir target --base-name Win32GUI --include-modules wx,pcapy

deploy:
	cp src/horn.ico target/
	cp src/WinPcap_4_1_3.exe target/
	cp README.txt target/
	7z a -tzip oblivion.zip target/
	scp -P 8912 oblivion.zip whoknowwhat@drunkenhaze.org:~/project/oblivion-service/static/oblivion.zip
	rm oblivion.zip

clean:
	rm -rf target/*
