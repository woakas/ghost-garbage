package com.tesis;

import java.io.IOException;
import java.util.Enumeration;
import java.util.Hashtable;

import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.AlertType;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;
import javax.microedition.lcdui.StringItem;
import javax.microedition.midlet.MIDlet;

import org.json.me.JSONArray;
import org.json.me.JSONException;
import org.json.me.JSONObject;

import vista.GhostGarbage;
import vista.Padre;
import vista.Lista;

import Logica.ConnectHttp;

import com.nutiteq.MapItem;
import com.nutiteq.components.Line;
import com.nutiteq.components.LineStyle;
import com.nutiteq.components.Place;
import com.nutiteq.components.PlaceIcon;
import com.nutiteq.components.WgsPoint;
import com.nutiteq.controls.ControlKeys;
import com.nutiteq.listeners.PlaceListener;
import com.nutiteq.location.LocationMarker;
import com.nutiteq.location.LocationSource;
import com.nutiteq.location.NutiteqLocationMarker;
import com.nutiteq.location.providers.LocationAPIProvider;

public class Map implements CommandListener, PlaceListener {
	private Form mMainForm;
	private MapItem mapItem;
	private Command regresar, menu, identificar,inventario, servicios, gps;
	private Display display;
	private Displayable next;
	private Padre identify, sgps;
	private Lista inventory,services;
	private Hashtable icons = new Hashtable();
	private Hashtable places= new Hashtable();
	private String key = "fe131d7f5a6b38b23cc967316c13dae24aef25e2a8e067.74529412";
	private StringItem message, puntaje, estado,vision;
	private Alert alert;
	private static int zoom = 17;

	public Map(MIDlet midlet, final Display display, Displayable next) {
		this.display = display;
		this.next = next;
		puntaje= new StringItem("Puntaje","0");
		estado= new StringItem("Estado","");
		vision= new StringItem("Rango de Visión","0");
		mapItem = new MapItem("Mapa", key, midlet, 300, 150, new WgsPoint(
				-74.09626007080078, 4.652224439717772), zoom);
		mapItem.defineControlKey(ControlKeys.MOVE_UP_KEY, Canvas.KEY_NUM2);
		mapItem.defineControlKey(ControlKeys.MOVE_DOWN_KEY, Canvas.KEY_NUM8);
		mapItem.defineControlKey(ControlKeys.MOVE_LEFT_KEY, Canvas.KEY_NUM4);
		mapItem.defineControlKey(ControlKeys.MOVE_RIGHT_KEY, Canvas.KEY_NUM6);
		mapItem.defineControlKey(ControlKeys.ZOOM_IN_KEY, Canvas.KEY_POUND);
		mapItem.defineControlKey(ControlKeys.ZOOM_OUT_KEY, Canvas.KEY_STAR);
		// define a Control Key para seleccionar un sitio
		mapItem.defineControlKey(ControlKeys.SELECT_KEY, -5);
		menu = new Command("Menu Principal", Command.EXIT, 2);
		regresar = new Command("Regresar", Command.OK, 1);
		identificar = new Command("Identificar", Command.OK, 1);
		inventario = new Command("Inventario", Command.OK, 1);
		servicios = new Command("Acceder Servicios", Command.OK, 1);
		gps = new Command("Posición GPS", Command.OK, 1);
		mMainForm = new Form("Ghost Garbage");
		mMainForm.append(mapItem);
		mMainForm.addCommand(menu);
		mMainForm.addCommand(regresar);
		mMainForm.addCommand(identificar);
		mMainForm.addCommand(inventario);
		mMainForm.addCommand(servicios);
		mMainForm.addCommand(gps);
		mMainForm.setCommandListener(this);
		mapItem.startMapping();
		message = new StringItem("", "");
		mMainForm.append(message);
		mMainForm.append(puntaje);
		mMainForm.append(estado);
		mMainForm.append(vision);

		// Para celulares con touch screen
		final Canvas canvas = new Canvas() {
			protected void paint(Graphics arg0) {
			}
		};

		final boolean pointer = canvas.hasPointerEvents();
		if (pointer)
			mapItem.showDefaultControlsOnScreen(true);
		else
			mapItem.showDefaultControlsOnScreen(false);
		try {
			Image icon = Image.createImage("/casita.png");
			icons.put("/casita.png",icon);
		} catch (IOException e) {
		}

		// linea
		WgsPoint[] linePoints = {
		};

		final Line line = new Line(linePoints, new LineStyle(0xFF0000, 5));
		mapItem.addLine(line);

		// definir la clase de escucha para los Places
		mapItem.setPlaceListener(this);

		// Mostrar Localizacion gps
		if (System.getProperty("microedition.location.version") != null) {
			final LocationSource dataSource = new LocationAPIProvider(4000) {
				public WgsPoint getLocation() {
					WgsPoint wp = super.getLocation();
					GhostGarbage.LONGPS = wp.getLon();
					GhostGarbage.LATGPS = wp.getLat();
					String body = ConnectHttp
					.getUrlBody(vista.GhostGarbage.URLGHOST
							+ "mobile/position/" + wp.getLon() + "/"
							+ wp.getLat() + "/");
					//System.out.println(body);
					try {
						if (body != null) {
							JSONObject js = new JSONObject(body);
							wp = new WgsPoint(Double.parseDouble(js.getString("lon")), 
									Double.parseDouble(js.getString("lat")));
							mapItem.mapMoved();
							if (js.optBoolean("puntaje_change",false)){
								puntaje.setText(js.optString("puntaje",puntaje.getText()));
							}
							if (js.optBoolean("vision_change",false)){
								vision.setText(js.optString("vision",vision.getText()));
							}
							if (js.optBoolean("estado_change",false)){
								estado.setText(js.optString("estado",estado.getText()));
							}
							if (js.optString("messageAlert",null)!= null){
								Image img1 = null;
								try {
									img1 = Image.createImage("/"+js.getString("iconAlert"));
								} catch (IOException e) {}
								alert = new Alert ("Mensaje", js.getString("messageAlert"), img1,AlertType.ERROR);
								display.setCurrent(alert);
								display.vibrate(2);
							}
						}else {
							wp=new WgsPoint(vista.GhostGarbage.LON_DEFAULT,vista.GhostGarbage.LAT_DEFAULT);
						}
						
						JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST + "data/json/");
						if (js.optString("status").equals("OK")){							
						JSONArray jsa = js.optJSONArray("places");
						Place [] pls = new Place[jsa.length()];
						Hashtable tempPlaces = new Hashtable();
						for (int i=0;i<jsa.length(); i++){							
							pls [i] = new Place(1, jsa.optJSONObject(i).optString("nombre","no name"), getImage(jsa.optJSONObject(i).optString("icon","/casita.png")),
									Double.parseDouble(jsa.optJSONObject(i).optString("lon","0.0")),Double.parseDouble(jsa.optJSONObject(i).optString("lat","0.0")));
							tempPlaces.put(jsa.optJSONObject(i).optString("id",""), pls[i]);
						}						
						mapItem.addPlaces(pls);
						for (Enumeration en = places.keys(); en.hasMoreElements();){
							String tt = (String) en.nextElement();
							Place p = (Place) places.get(tt);
							Place pt = (Place) tempPlaces.get(tt);
							if (pt==null){
								mapItem.removePlace(p);
							}
							else if(!((Place) places.get(tt)).getWgs().equals(((Place) tempPlaces.get(tt)).getWgs())){
								mapItem.removePlace((Place) places.get(tt));	
							}
						}
						places = tempPlaces; 
						}
						
					} catch (JSONException e) {	}
					return wp;
				}
			};
			try {
				final Image gpsPresentImage = Image
				.createImage("/casita.png");
				final Image gpsConnectionLost = Image
				.createImage("/banderinrojo.png");
				final LocationMarker marker = new NutiteqLocationMarker(
						new PlaceIcon(gpsPresentImage, 4, 16), new PlaceIcon(
								gpsConnectionLost, 4, 16), 0, true);
				dataSource.setLocationMarker(marker);
				mapItem.setLocationSource(dataSource);
			} catch (final IOException e) {
			}
		}
	}

	public void placeClicked(final Place p) {
		message.setText("Click ID: " + p.getId() + "Nombre del Sitio: "
				+ p.getName()+"\n");
	}

	public void placeEntered(final Place p) {
		message.setText("Entered ID: " + p.getId() + "Nombre del Sitio: "
				+ p.getName()+"\n");
	}

	public void placeLeft(final Place p) {
		message.setText("Izquierda ID : " + p.getId() + "Nombre del Sitio"
				+ p.getName()+"\n");
	}

	public void commandAction(Command c, Displayable d) {
		if (c.getLabel() =="Menu Principal") {
			display.setCurrent(next);
		}
		else if (c.getLabel() =="Regresar") {

		}  
		else if (c.getLabel() =="Acceder Servicios") {
			try {
				JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST+"/mobile/services/");
				JSONArray jsa = js.optJSONArray("services");
				String aux [] = new String [jsa.length()];
				for (int i=0;i<jsa.length(); i++){
					aux[i] = jsa .optString(i,"");
				}
				services= new vista.Lista(display,this.call(),aux,"tienda.png","logoj.png","Enviar");
			} catch (IOException e) {
			}
			display.setCurrent(services);
		}
		else if (c.getLabel() =="Identificar") {
			try {
				JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST+"/mobile/identifyServices/");
				identify = new vista.Padre(display,this.call(),js.optString("services", "No hay servicios Cercanos"),"identificar.png","logoj.png", "Identificar");
			} catch (IOException e) {
			}
			display.setCurrent(identify);
		} else if (c.getLabel() =="Inventario") {
			try {
				JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST+"/mobile/inventory/");
				JSONArray jsa = js.optJSONArray("services");
				String aux [] = new String [jsa.length()];
				for (int i=0;i<jsa.length(); i++){
					aux[i] = jsa .optString(i,"");
				}
				inventory = new vista.Lista(display,this.call(),aux,"inventario.png","logoj.png","Activar");
			}
			catch (IOException e) {
			}
			display.setCurrent(inventory);
		}
		else if (c.getLabel() =="Posición GPS") {
			    String info = "Longitud: " + GhostGarbage.LONGPS + "\nLatidud: " + GhostGarbage.LATGPS;
				try {
					sgps = new vista.Padre(display,this.call(),info,"gps.png","logoj.png", "Identificar");
				} catch (IOException e) {}
			display.setCurrent(sgps);
		}
	}
	public String getPuntaje(){
		return puntaje.getText();
	}
	public void setPuntaje(String estado){
		this.puntaje.setText(estado);
	}
	public String getEstado(){
		return estado.getText();
	}
	public void setEstado(String estado){
		this.estado.setText(estado);
	}
	public String getVision(){
		return vision.getText();
	}
	public void setVision(String estado){
		this.vision.setText(estado);
	}
	public MapItem getMapItem(){
		return mapItem;
	}
	public Form call() {
		return mMainForm;
	}
	protected Image getImage(String url){
		Image n = (Image) icons.get(url);
		if (n == null){
			try {
				n = Image.createImage(url);
				icons.put(url, n);
			} catch (IOException e) {
				return (Image) icons.get("/casita.png");
			}
		}
		return n;		
	}
}
