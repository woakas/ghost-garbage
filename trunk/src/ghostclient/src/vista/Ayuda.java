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
	public String text="Ghost Garbage es un juego el cual se basa en técnología LBS para determinar puntos cercanos y sevicios asociados directamente a la posición de la persona espacialmente";
				
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