package vista;

import java.io.IOException;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.StringItem;

public class Informacion extends Form implements CommandListener {
	private Display display;
	private Displayable next;
	private StringItem ayuda;
	private Command regresar;
	public String text="Ghost Garbage es un juego el cual se basa en tecnología LBS para determinar puntos cercanos y servicios asociados directamente a la posición de la persona espacialmente.";
				
	public Informacion (Display display, Displayable next) throws IOException{
	super("Informacion");
	ayuda= new StringItem("",text);
	regresar=new Command("Regresar",Command.BACK,1);
	append(new InformacionFiguras(null, this));
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