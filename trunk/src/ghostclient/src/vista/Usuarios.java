package vista;

import java.io.IOException;
import java.util.Timer;
import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.AlertType;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Gauge;
import javax.microedition.lcdui.Image;
import javax.microedition.lcdui.TextField;

import Logica.*;
import com.tesis.Map;

public class Usuarios extends Form implements CommandListener {
	public Gauge load;
	private Display display;
	private Displayable next;
	private Map mapa;
	private TextField password,usuario;
	private Command ingresar, regresar;
	private Alert alert;
	private Timer tm;
	private Progreso pr;
			
	public Usuarios (Display display, Displayable next,  Image image1 ,Map mapa) throws IOException{
	super("Login");
	usuario= new TextField("Usuario","",30,TextField.ANY);
	password= new TextField("Password","",30,TextField.PASSWORD);
	ingresar=new Command("Ingresar",Command.SCREEN,2);
	regresar=new Command("Regresar",Command.BACK,1);
	load = new Gauge(null,false,20,1);
	alert = new Alert ("Error de Logeo", "              Usuario o Contrasena no valida", image1 ,AlertType.ERROR);
	append(new Figuras(null, this));
	append(usuario);
	append(password);
	append(load);
	this.mapa = mapa;
	this.next = next;
	this.display = display;
	addCommand(ingresar);
	addCommand(regresar);
	setCommandListener(this);
	}
	
	public void commandAction(Command co, Displayable d){
		if (co==ingresar){
			tm = new Timer();
			pr = new Progreso(load);
			tm.scheduleAtFixedRate(pr, 0, 1000);
			if (ConnectHttp.getUrl(vista.GhostGarbage.URLGHOST+"mobile/login",usuario.getString(),password.getString()) == null){
				System.out.println("prueba1 " +ConnectHttp.getUrl(vista.GhostGarbage.URLGHOST+"mobile/login"));
				display.setCurrent(alert);
				display.vibrate(2);
			}
			else{
				System.out.println("prueba1 " +ConnectHttp.getUrl(vista.GhostGarbage.URLGHOST+"mobile/login"));
				display.setCurrent(mapa.call());
			} 
		}
		else if (co==regresar){
			display.setCurrent(next); 
		}
	}
}