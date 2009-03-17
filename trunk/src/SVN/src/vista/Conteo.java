package vista;

import java.util.TimerTask;

class Conteo extends TimerTask {
	private final Intro intro;
	Conteo(Intro intro) {
	this.intro = intro;
	}
	public void run() {
	Intro.access(this.intro);
	}
}
