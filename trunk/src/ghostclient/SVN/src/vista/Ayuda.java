package vista;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Font;
import javax.microedition.lcdui.Graphics;


public final class Ayuda extends Canvas implements CommandListener{
	
	private Display display;
	private Displayable next;
	private Command seguir, regresar;
	
	
	public Ayuda(Display display, Displayable next) {
	seguir=new Command("Seguir",Command.SCREEN,1);
	regresar=new Command("Regresar",Command.BACK,2);
	this.display = display;
	this.next = next;
	display.setCurrent(this);
	addCommand(seguir);
	addCommand(regresar);
	setCommandListener(this);
}
	
		
		protected void paint(Graphics g) {
		g.setColor(125, 125, 125);
	    g.fillRect (0, 0, getWidth(), getHeight()); 
	    Font fuente = Font.getFont(Font.FACE_SYSTEM, Font.STYLE_BOLD, Font.SIZE_LARGE);
		g.setFont(fuente);
		g.setColor(255, 255, 255);
		g.drawString ("Hola Mundo. asdqwertyuiopasdfghjkl", 0 , 0, Graphics.LEFT | Graphics.TOP);
		}

		public void commandAction(Command c, Displayable s) {
			if (c==seguir){
				System.out.println("Sirve");	
			}
			else if (c==regresar){
				display.setCurrent(next); 
			}
			display.setCurrent(this); 			
		}
	
}