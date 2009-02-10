package vista;

import javax.microedition.lcdui.*;

public class Informacion extends Form implements CommandListener{
	private Command seguir, regresar;
	private Display display;
	private Displayable next;
	private StringItem st;
	
	public Informacion (Display display, Displayable next){
	super("Informacion");
	st= new StringItem("Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaa","");
	seguir=new Command("Seguir",Command.SCREEN,1);
	regresar=new Command("Regresar",Command.BACK,2);
	this.append(st);
	this.display = display;
	this.next = next;
	display.setCurrent(this);
	addCommand(seguir);
	addCommand(regresar);
	setCommandListener(this);
	}
	
	public void commandAction(Command c, Displayable d){
		if (c==seguir){
			System.out.println("Sirve");	
		}
		else if (c==regresar){
			display.setCurrent(next); 
		}
		display.setCurrent(this); 			
	}
}
