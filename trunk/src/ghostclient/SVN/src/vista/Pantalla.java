package vista;

import java.io.IOException;

import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Image;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

public class Pantalla extends MIDlet {
	
	int opcion;
		
	private Display p;
	private Presentacion pres;
	private Form f;
	private Intro intro;
	private Ayuda ayuda;
	private Informacion informacion;
	private Image img;
			
	public Pantalla() throws IOException {
		f = new Form("Ghost Garbage");
		f.append(new BotonIni("Inicio", f));
		p = Display.getDisplay(this);
		pres = new Presentacion(this);
		img = Image.createImage("/decarta.png");
		intro = new Intro(p, pres, img, 5000);
		ayuda = new Ayuda(p, pres);
		informacion = new Informacion(p, pres);
	}
	
	
	public void getOpcion(int opcion) {
		this.opcion = opcion;
		if(opcion == 1){
			p.setCurrent(intro);
		}
		if(opcion == 2){
			p.setCurrent(informacion);
		}
		if(opcion == 3){
			p.setCurrent(ayuda);
		}
		if(opcion == 4){
			notifyDestroyed();
		}
	}
	protected void destroyApp(boolean arg0) throws MIDletStateChangeException {
	}
	protected void pauseApp() {
	}
	protected void startApp() throws MIDletStateChangeException {
		p.setCurrent(intro);
	}
}
