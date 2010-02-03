package com.tesis;

import java.io.IOException;

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

import org.json.me.JSONException;
import org.json.me.JSONObject;

import vista.Padre;
import vista.Inventario;

import Logica.ConnectHttp;

import com.nutiteq.MapItem;
import com.nutiteq.components.Line;
import com.nutiteq.components.LineStyle;
import com.nutiteq.components.Place;
import com.nutiteq.components.PlaceIcon;
import com.nutiteq.components.WgsBoundingBox;
import com.nutiteq.components.WgsPoint;
import com.nutiteq.controls.ControlKeys;
import com.nutiteq.kml.KmlUrlReader;
import com.nutiteq.listeners.PlaceListener;
import com.nutiteq.location.LocationMarker;
import com.nutiteq.location.LocationSource;
import com.nutiteq.location.NutiteqLocationMarker;
import com.nutiteq.location.providers.LocationAPIProvider;

public class Map implements CommandListener, PlaceListener {
	private Form mMainForm;
	private MapItem mapItem;
	private Command regresar, menu, identificar,inventario, servicios;
	private Display display;
	private Displayable next;
	private Padre identify;
	private Inventario inventory;
	private Image icon;
	private String key = "fe131d7f5a6b38b23cc967316c13dae24aef25e2a8e067.74529412";
	private StringItem message, puntaje, estado;
	private Alert alert;
	private static int zoom = 17;

	//KmlUrlReader pp;

	public Map(MIDlet midlet, final Display display, Displayable next) {
		this.display = display;
		this.next = next;
		puntaje= new StringItem("Puntaje","0");
		estado= new StringItem("Estado","");
		/*pp = new KmlUrlReader(
				//"http://library.devnull.li/cgi-bin/featureserver.cgi/scribble/all.kml",
				vista.GhostGarbage.URLGHOST+"data/kml/",
				true) {
			public boolean needsUpdate(WgsBoundingBox boundingBox, int zoom) {
				return true;
			}
		};*/
		mapItem = new MapItem("Mapa", key, midlet, 300, 150, new WgsPoint(
				-74.09626007080078, 4.652224439717772), zoom);
		//mapItem.addKmlService(pp);
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
		mMainForm = new Form("Ghost Garbage");
		mMainForm.append(mapItem);
		mMainForm.addCommand(menu);
		mMainForm.addCommand(regresar);
		mMainForm.addCommand(identificar);
		mMainForm.addCommand(inventario);
		mMainForm.addCommand(servicios);
		mMainForm.setCommandListener(this);
		mapItem.startMapping();
		message = new StringItem("", "");
		mMainForm.append(message);
		mMainForm.append(puntaje);
		mMainForm.append(estado);

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
			icon = Image.createImage("/casita.png");
		} catch (IOException e) {
		}
		mapItem.addPlace(new Place(1, "Casita", icon, vista.GhostGarbage.LON_DEFAULT,
				vista.GhostGarbage.LAT_DEFAULT));

		// linea
		WgsPoint[] linePoints = {
		// new WgsPoint(-74.13538813591003, 4.630740894173603),
		// new WgsPoint(-74.13138813591003, 4.631740894173603),
		};

		final Line line = new Line(linePoints, new LineStyle(0xFF0000, 5));
		mapItem.addLine(line);

		// definir la clase de escucha para los Places
		mapItem.setPlaceListener(this);

		// adicionar Layer KML al mapa con Panoramio
		// prueba
		// KmlUrlReader pp= new
		// KmlUrlReader("http://library.devnull.li/featureserver/prueba.kml",true);
		// KmlUrlReader pp= new
		// KmlUrlReader("http://library.devnull.li/cgi-bin/featureserver.cgi/scribble/all.kml",true);
		// mapItem.addKmlService(new
		// KmlUrlReader("http://map.elphel.com/Elphel_Cameras.kml",true));
		// mapItem.addKmlService(new
		// KmlUrlReader("http://www.panoramio.com/panoramio.kml?LANG=en_US.utf8",true));
		// mapItem.addKmlService(pp);

		// Mostrar Localizacion gps
		if (System.getProperty("microedition.location.version") != null) {
			final LocationSource dataSource = new LocationAPIProvider(7000) {
				public WgsPoint getLocation() {
					WgsPoint wp = super.getLocation();
					String body = ConnectHttp
							.getUrlBody(vista.GhostGarbage.URLGHOST
									+ "mobile/position/" + wp.getLon() + "/"
									+ wp.getLat() + "/");
					System.out.println(body);
					try {
						if (body != null) {
							JSONObject js = new JSONObject(body);
							wp = new WgsPoint(Double.parseDouble(js.getString("lon")), 
									Double.parseDouble(js.getString("lat")));
							mapItem.getZoom();
							mapItem.getZoomRange();
							if (js.optBoolean("puntaje_change",false)){
								puntaje.setText(js.optString("puntaje",puntaje.getText()));
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
					} catch (JSONException e) {
						e.printStackTrace();
					}
					
					return wp;
				}
			};
			try {
				final Image gpsPresentImage = Image
						.createImage("/banderinazul.png");
				final Image gpsConnectionLost = Image
						.createImage("/banderinrojo.png");
				final LocationMarker marker = new NutiteqLocationMarker(
						new PlaceIcon(gpsPresentImage, 4, 16), new PlaceIcon(
								gpsConnectionLost, 4, 16), 0, true);
				dataSource.setLocationMarker(marker);
				System.out.println("Cualquier cosa");
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
		if (c == menu) {
			display.setCurrent(next);
		}
		else if (c == regresar) {

		}  
		else if (c == servicios) {

		}
		else if (c == identificar) {
			try {
				JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST+"/mobile/identifyServices/");
				identify = new vista.Padre(display,this.call(),js.optString("services", "No hay servicios Cercanos"),"identificar.png","logoj.png", "Identificar");
			} catch (IOException e) {
			}
			display.setCurrent(identify);
		} else if (c == inventario) {
			try {
				//JSONObject js = ConnectHttp.getUrlJson(vista.GhostGarbage.URLGHOST+"/mobile/inventory/");
				inventory = new vista.Inventario(display,this.call(),"escobita.png","fantasma.png");
				//inventory = new vista.Padre(display,this.call(),js.optString("services", "No Tiene nada en su inventario"),"inventario.png","logoj.png", "Inventario actual");
			} catch (IOException e) {
			}
			display.setCurrent(inventory);
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
	public MapItem getMapItem(){
		return mapItem;
	}
	public Form call() {
		return mMainForm;
	}	
}
