package vista;

import java.io.IOException;

import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.AlertType;
import javax.microedition.lcdui.ChoiceGroup;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Image;

import org.json.me.JSONArray;
import org.json.me.JSONException;
import org.json.me.JSONObject;

import Logica.ConnectHttp;

public class Lista extends Form implements CommandListener { 
	private Display display;
	private Displayable next;
	private ChoiceGroup inventario;

	public Lista (Display display, Displayable next,String [] inventory,String image, String image2, String comando) throws IOException{
		super("Inventario");
		append(new PadreFiguras(null, this, image,image2));
		inventario =new ChoiceGroup("Inventario",ChoiceGroup.EXCLUSIVE,inventory,null);
		append(inventario);
		this.next = next;
		this.display = display;
		Command regresar = new Command("Regresar",Command.BACK,2);
		Command salvar = new Command(comando,Command.ITEM,1);
		addCommand(regresar);
		addCommand(salvar);
		setCommandListener(this);
	}

	public void commandAction(Command c, Displayable d){
		if (c.getLabel() == "Enviar"){
			JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST+"/mobile/services/"+inventario.getString(inventario.getSelectedIndex())+"/");
			JSONArray jsa = js.optJSONArray("services");
			String aux [] = new String [jsa.length()];
			for (int i=0;i<jsa.length(); i++){
				aux[i] = jsa .optString(i,"");
			}
			try {
				Lista services= new Lista(display,next,aux,"escobita.png","fantasma.png","Salvar");
				display.setCurrent(services);
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		
		if (c.getLabel() =="Activar"){
			JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST+"/mobile/inventory/"+inventario.getString(inventario.getSelectedIndex())+"/");
			Alert alert;
			Image img1 = null;
			try {
				img1 = Image.createImage("/"+js.getString("iconAlert"));
				alert = new Alert ("Activo",js.getString("messageAlert"),img1 ,AlertType.INFO);
				display.setCurrent(alert,next);
				display.vibrate(2);
			}catch (JSONException e) {	}
			  catch (IOException e)   {	}
		}
		
		if (c.getLabel() =="Salvar"){
			
		}
		if (c.getLabel() =="Regresar"){
			display.setCurrent(next); 
		}
	}
}
