package vista;

import java.io.IOException;

import javax.microedition.lcdui.ChoiceGroup;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Image;
import javax.microedition.lcdui.List;
import javax.microedition.lcdui.TextField;

import com.tesis.*;



public class Usuarios extends Form implements CommandListener {
	
	private Command ingresar, regresar;
	private Display display;
	private Displayable next;
    private HelloMap mapa;
	private TextField password;
	private ChoiceGroup usuario;
	
	public Usuarios (Display display, Displayable next, Image image, Image image2 ,HelloMap mapa) throws IOException{
	super("Usuarios");
	String opciones[] = {"Escobita","Ghost"};
	password= new TextField("Password","",30,TextField.PASSWORD);
	usuario=new ChoiceGroup("Muneco",List.EXCLUSIVE,opciones,null);
	ingresar=new Command("Ingresar",Command.SCREEN,2);
	regresar=new Command("Regresar",Command.BACK,1);
	this.append(new Figuras("Login", this));
	this.append(usuario);
	this.append(password);
	this.mapa = mapa;
	this.next = next;
	this.display = display;
	addCommand(ingresar);
	addCommand(regresar);
	setCommandListener(this);
	}
	
	public void commandAction(Command c, Displayable d){
		if (c==ingresar){
			int opcionelegida = usuario.getSelectedIndex();
			 //salvar opciones en memoria persistente.
			System.out.println("Opcion elegida nº"+(opcionelegida+1));
			display.setCurrent(mapa.call());
		}
		else if (c==regresar){
			display.setCurrent(next); 
		}
		display.setCurrent(this); 	
	}
}