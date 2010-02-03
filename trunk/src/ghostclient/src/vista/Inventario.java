package vista;

import java.io.IOException;
import javax.microedition.lcdui.ChoiceGroup;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;

public class Inventario extends Form implements CommandListener { 
	private Display display;
	private Displayable next;
	private Command salvar,regresar;
	private ChoiceGroup inventario;

	public Inventario (Display display, Displayable next,String image, String image2) throws IOException{
		super("Inventario");
		String []inventory ={"uno","dos","tres","cuatro","ETC"};
		append(new PadreFiguras(null, this, image,image2));
		inventario =new ChoiceGroup("Inventario",ChoiceGroup.EXCLUSIVE,inventory,null);
		append(inventario);
		this.next = next;
		this.display = display;
		regresar = new Command("Regresar",Command.BACK,2);
		salvar = new Command("Salvar",Command.ITEM,1);
		addCommand(regresar);
		addCommand(salvar);
		setCommandListener(this);
	}

	public void commandAction(Command c, Displayable d){
		if (c == salvar){
			System.out.println(inventario.getString(inventario.getSelectedIndex()));	
				display.setCurrent(next);	
			
		}
		if (c==regresar){
			display.setCurrent(next); 
		}
	}
}
