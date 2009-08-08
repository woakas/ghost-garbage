package com.tesis;

import java.io.IOException;

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

import com.nutiteq.MapItem;
import com.nutiteq.components.Line;
import com.nutiteq.components.LineStyle;
import com.nutiteq.components.Place;
import com.nutiteq.components.PlaceIcon;
import com.nutiteq.components.WgsPoint;
import com.nutiteq.controls.ControlKeys;
import com.nutiteq.kml.KmlService;
import com.nutiteq.kml.KmlUrlReader;
import com.nutiteq.listeners.PlaceListener;
import com.nutiteq.location.LocationMarker;
import com.nutiteq.location.LocationSource;
import com.nutiteq.location.NutiteqLocationMarker;
import com.nutiteq.location.providers.LocationAPIProvider;

public class Map  implements CommandListener,PlaceListener{
private Form mMainForm;
private MapItem mapItem;
private Command regresar, menu, arrojar, poder;
private Display display;
private Displayable next;
private Image icon;
private StringItem message;
private static int zoom=12;

	public Map(MIDlet midlet, Display display, Displayable next ) {
		this.display = display;
		this.next = next;
		mapItem = new MapItem("Mapa", "Tesis", midlet, 300, 150, new WgsPoint(-74.09626007080078,4.652224439717772), zoom);
		mapItem.defineControlKey(ControlKeys.MOVE_UP_KEY, Canvas.KEY_NUM2);
		mapItem.defineControlKey(ControlKeys.MOVE_DOWN_KEY, Canvas.KEY_NUM8);
		mapItem.defineControlKey(ControlKeys.MOVE_LEFT_KEY, Canvas.KEY_NUM4);
		mapItem.defineControlKey(ControlKeys.MOVE_RIGHT_KEY, Canvas.KEY_NUM6);
		mapItem.defineControlKey(ControlKeys.SELECT_KEY, Canvas.KEY_POUND);
		mapItem.defineControlKey(ControlKeys.SELECT_KEY, Canvas.KEY_STAR);
		//define a Control Key para seleccionar un sitio 
		mapItem.defineControlKey(ControlKeys.SELECT_KEY, -5);
		
		menu=new Command("Menu Principal",Command.EXIT,2);
		regresar=new Command("Regresar",Command.OK,1);
		poder=new Command("Poder",Command.OK,1);
		arrojar=new Command("Arrojar",Command.OK,1);
		mMainForm =new Form ("Ghost Garbage");
		mMainForm.append(mapItem);		
		mMainForm.addCommand(menu);
		mMainForm.addCommand(regresar);
		mMainForm.addCommand(arrojar);
		mMainForm.addCommand(poder);
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
	       //prueba 
	       //KmlUrlReader pp= new KmlUrlReader("http://library.devnull.li/featureserver/prueba.kml",true);
	       KmlUrlReader pp= new KmlUrlReader("http://library.devnull.li/cgi-bin/featureserver.cgi/scribble/all.kml",true);
	       //mapItem.addKmlService(new KmlUrlReader("http://map.elphel.com/Elphel_Cameras.kml",true));
	       //mapItem.addKmlService(new KmlUrlReader("http://www.panoramio.com/panoramio.kml?LANG=en_US.utf8",true));
	       mapItem.addKmlService(pp);
	       
	       //mostrar Localizacion gps
	       if(System.getProperty("microedition.location.version")!= null){
	    	   final LocationSource dataSource = new LocationAPIProvider(3000);
	    	   try{
	    		   final Image gpsPresentImage = Image.createImage("/banderinazul.png");
	    		   final Image gpsConnectionLost = Image.createImage("/banderinrojo.png");
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
	

	public void commandAction (Command c, Displayable d){
		if(c==menu){
			display.setCurrent(next); 			
		} 
		
		else if (c==regresar){
			//zoom = 2;
			KmlService kk[]= new KmlService[mapItem.getKmlServices().length];
			for (int i=0; i < mapItem.getKmlServices().length; i ++){
				kk [i]= mapItem.getKmlServices()[i]; 				
			}
			for (int i=0; i < kk.length; i ++){
				mapItem.removeKmlService(kk[i]);
			}
			for (int i=0; i < kk.length; i ++){
				mapItem.addKmlService(kk[i]);
			}
		}		
	} 
	public Form call(){
		return mMainForm;
		
	}
}