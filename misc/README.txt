 ----------------------- [ RMMOEM ] -----------------------

[ A weboldal backend működéséhez szükséges telepíteni pár külső programot. A lépések a következők: ]

	1. Python 3.9+ telepítése
	2. PiP 22.3+ telepítése
	3. Külső könyvtárak telepítése:
		> pip install -r requirements.txt

[ Ha ezekkel készen vagyunk, terminálból elindíthatjuk az api szervert a következő parancsal: ]
		> python api.py

[ Ezután a frontend szervert elindíthatjuk több féle módon: ]
	1. Visual Studio Code live server funkcióját használva
	2. Pythonnal a weboldal mappájából:
		>python -m http.server
	3. Apache szerverrel, XAMPP-al