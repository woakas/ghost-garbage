package com.tesis;

import javax.microedition.midlet.MIDlet;
//import javax.microedition.midlet.MIDletStateChangeException;
import javax.microedition.lcdui.*;
import com.nutiteq.MapItem;
//import com.nutiteq.maps.*;
import com.nutiteq.components.WgsPoint;
import com.nutiteq.controls.ControlKeys;
import java.io.IOException;
import com.nutiteq.components.Place;
import com.nutiteq.components.Line;
import com.nutiteq.components.LineStyle;
import com.nutiteq.listeners.PlaceListener;
//KML
import com.nutiteq.kml.*;
//paquetes de localizacion
import com.nutiteq.location.LocationMarker;
import com.nutiteq.location.LocationSource;
import com.nutiteq.location.providers.LocationAPIProvider;
import com.nutiteq.location.NutiteqLocationMarker;
import com.nutiteq.components.PlaceIcon; 

public class HelloMap  implements CommandListener,PlaceListener{
private Form mMainForm;
private MapItem mapItem;
private Command regresar, menu;
private Display display;
private Displayable next;
private Image icon;
private StringItem message;

	
	public HelloMap(MIDlet midlet, Display display, Displayable next ) {
		this.display = display;
		this.next = next;
		regresar=new Command("Regresar",Command.EXIT,1);
		menu=new Command("Menu",Command.BACK,2);
		mapItem = new MapItem("Map", "tutorial", midlet, 300, 150, new WgsPoint(-74.09626007080078,4.652224439717772), 12);
		mapItem.defineControlKey(ControlKeys.MOVE_UP_KEY, Canvas.KEY_NUM2);
		mapItem.defineControlKey(ControlKeys.MOVE_UP_KEY, Canvas.UP);
		mapItem.defineControlKey(ControlKeys.MOVE_DOWN_KEY, Canvas.KEY_NUM8);
		mapItem.defineControlKey(ControlKeys.MOVE_DOWN_KEY, Canvas.DOWN);
		mapItem.defineControlKey(ControlKeys.MOVE_LEFT_KEY, Canvas.KEY_NUM4);
		mapItem.defineControlKey(ControlKeys.MOVE_LEFT_KEY, Canvas.LEFT);
		mapItem.defineControlKey(ControlKeys.MOVE_RIGHT_KEY, Canvas.KEY_NUM6);
		mapItem.defineControlKey(ControlKeys.MOVE_RIGHT_KEY, Canvas.RIGHT);
		//define a Control Key para seleccionar un sitio 
		mapItem.defineControlKey(ControlKeys.SELECT_KEY, -5);
		
		mMainForm =new Form ("Ghost Garbage");
		//mMainForm.append(new StringItem(null, "Hello, map!"));
		mMainForm.append(mapItem);
		mMainForm.addCommand(menu);
		mMainForm.addCommand(regresar);
		mMainForm.setCommandListener(this);
		mapItem.startMapping();
		message = new StringItem("","");
		mMainForm.append(message);
		
		// Para celulares con touch screen
		final Canvas canvas = new Canvas() {
			protected void paint(Graphics arg0) {	}
			};
			
			final boolean pointer = canvas.hasPointerEvents();
			if(pointer)
				mapItem.showDefaultControlsOnScreen(true);
				else
				mapItem.showDefaultControlsOnScreen(false);
			try {icon=Image.createImage("/casita.png");}
			catch(IOException e){}
			mapItem.addPlace(new Place(1, "Casita",icon,-74.13538813591003, 4.630740894173603 ));
			
			//linea 
			WgsPoint[] linePoints={
				//	new WgsPoint(-74.13538813591003, 4.630740894173603),
				//	new WgsPoint(-74.13138813591003, 4.631740894173603),
			};
	       
	       final Line line = new Line(linePoints, new LineStyle(0xFF0000, 5));
	       mapItem.addLine(line);
	       
	       //definir la clase de escucha para los Places
	       mapItem.setPlaceListener(this);
	       //adicionar Layer KML al mapa con Panoramio
	       mapItem.addKmlService(new KmlUrlReader("http://www.panoramio.com/panoramio.kml?LANG=en_US.utf8",true));
	       
	       //mostrar Localizacion gps
	       if(System.getProperty("microedition.location.version")!= null){
	    	   final LocationSource dataSource = new LocationAPIProvider(3000);
	    	   try{
	    		   final Image gpsPresentImage = Image.createImage("/presenteGps.png");
	    		   final Image gpsConnectionLost = Image.createImage("/perdidaGps.png");
	    		   final LocationMarker marker = new NutiteqLocationMarker(new PlaceIcon(gpsPresentImage, 4, 16),
	    				   new PlaceIcon(gpsConnectionLost, 4, 16),3000, true);
	    		   dataSource.setLocationMarker(marker);
	    		   mapItem.setLocationSource(dataSource);
	    		   } catch (final IOException e){}
	       }
	    		   
	      
	}
	
	public void placeClicked(final Place p){
		message.setText("Click ID: " + p.getId() + "Nombre del Sitio: " + p.getName());
	}
	
	public void placeEntered(final Place p){
		message.setText("Entered ID: " + p.getId() + "Nombre del Sitio: " + p.getName());
	}

	public void placeLeft(final Place p){
		message.setText("Izquierda ID : " + p.getId() + "Nombre del Sitio" + p.getName());
	}
	

	public void commandAction (Command c, Displayable s){
		if (c==menu){
			System.out.println("Sirve");	
		}
		else if (c==regresar){
			display.setCurrent(next); 
		}		
}
	public Form call(){
		return mMainForm;
		
	}
}
