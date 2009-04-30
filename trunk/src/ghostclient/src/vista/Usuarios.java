package vista;

import java.io.IOException;
import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.AlertType;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Gauge;
import javax.microedition.lcdui.Image;
import javax.microedition.lcdui.TextField;
import Logica.*;
import com.tesis.*;

public class Usuarios extends Form implements CommandListener {
	
	private Command ingresar, regresar;
	private Display display;
	private Displayable next;
    private HelloMap mapa;
	private TextField password,usuario;
	public Gauge load;
	private Alert alert;
			
	public Usuarios (Display display, Displayable next,  Image image1 ,HelloMap mapa) throws IOException{
	super("Login");
	usuario= new TextField("Usuario","",30,TextField.ANY);
	password= new TextField("Password","",30,TextField.PASSWORD);
	ingresar=new Command("Ingresar",Command.SCREEN,2);
	regresar=new Command("Regresar",Command.BACK,1);
	load = new Gauge(null,false,12,0);
	alert = new Alert ("Error de Logeo", "              Usuario o Contrasena no valida", image1 ,AlertType.ERROR);
	this.append(new Figuras(null, this));
	this.append(usuario);
	this.append(password);
	this.append(load);
	this.mapa = mapa;
	this.next = next;
	this.display = display;
	addCommand(ingresar);
	addCommand(regresar);
	setCommandListener(this);
	
	}
	
	public void commandAction(Command co, Displayable d){
		if (co==ingresar){
			load.setValue(4);
			load.getValue();
			
			//System.out.println("prueba " +ConnectHttp.getUrl("http://dev.ghost.webhop.org/mobile/login","ghost","garbage"));
			if (ConnectHttp.getUrl("http://dev.ghost.webhop.org/mobile/login",usuario.getString(),password.getString()) == null){
				load.setValue(8);
				display.setCurrent(this);
				System.out.println("prueba1 " +ConnectHttp.getUrl("http://dev.ghost.webhop.org/mobile/login"));
				load.setValue(12);
				display.setCurrent(alert);
			}
			else{
				System.out.println("prueba1 " +ConnectHttp.getUrl("http://dev.ghost.webhop.org/mobile/login"));
				display.setCurrent(mapa.call());
			} 
		}
		else if (co==regresar){
			display.setCurrent(next); 
		}
		display.setCurrent(this); 	
	}
}