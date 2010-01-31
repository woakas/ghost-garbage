package vista;

import java.io.IOException;

import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Image;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

import com.tesis.Map;

public class GhostGarbage extends MIDlet {
	
	int opcion;
	private Display p;
	private Presentacion pres;
	private Form f;
	private Intro intro;
	private Map mapa;
	private Ayuda ayuda;
	private Informacion informacion;
	private Image img, img1;
	private Usuarios usuarios;
	public static String URLGHOST = "http://dev1.ghost.webhop.org/";
	public static double LON_DEFAULT = -74.13538813591003;
	public static double LAT_DEFAULT = 4.630740894173603;
			
	public GhostGarbage() throws IOException {
		f = new Form("Ghost Garbage");
		f.append(new BotonIni("Inicio", f));
		p = Display.getDisplay(this);
		pres = new Presentacion(this);
        pres.setFullScreenMode(true);
		img = Image.createImage("/logogrup.png");
		img1 = Image.createImage("/cerrar.png");
		intro = new Intro(p, pres, img, 5000);
		
		mapa = new Map((MIDlet)(this), p, pres);
		usuarios = new Usuarios(p,pres,img1,mapa);
		ayuda = new Ayuda(p, pres);
		informacion = new Informacion(p, pres);
	}
		
	public void getOpcion(int opcion) {
		this.opcion = opcion;
		if(opcion == 1){
			p.setCurrent(usuarios);
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