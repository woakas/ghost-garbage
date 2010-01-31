package vista;

import java.io.IOException;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.StringItem;

public class Padre extends Form implements CommandListener {
	private Display display;
	private Displayable next;
	private StringItem padre;
	private Command regresar;
	
	public Padre (Display display, Displayable next, String mensaje, String image, String image2,String titulo ) throws IOException{
	super(titulo);
	padre= new StringItem("",mensaje);
	regresar=new Command("Regresar",Command.BACK,1);
	append(new PadreFiguras(null, this, image,image2));
	append(padre);
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