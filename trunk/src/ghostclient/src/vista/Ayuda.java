package vista;

import java.io.IOException;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.StringItem;

public class Ayuda extends Form implements CommandListener {
	private Display display;
	private Displayable next;
	private StringItem ayuda;
	private Command regresar;
	public String text="Ghost Garbage es un juego que consiste en recolectar la mayor cantidad de objetos los cuales aparecerán aleatoriamente en el mapa, consiguiéndolos al ir a cada uno de los sitios descritos de forma física antes de ser eliminado por un adversario. O existe otra opción la cual es eliminar al adversario de tal manera que no logre recolectar objetos, Para mayor información visite la página http://ghost.webhop.org/";				
	
	public Ayuda (Display display, Displayable next) throws IOException{
	super("Ayuda");
	ayuda= new StringItem("",text);
	regresar=new Command("Regresar",Command.BACK,1);
	append(new AyudaFiguras(null, this));
	append(ayuda);
	this.next = next;
	this.display = display;
	addCommand(regresar);
	setCommandListener(this);
	}
	
	public void commandAction(Command co, Displayable d){
		if (co==regresar){
			display.setCurrent(next); 
		}
	}
}