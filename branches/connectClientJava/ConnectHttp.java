import java.net.*;
import java.io.*;
import java.util.*;

public class ConnectHttp {
	
	private String cookie;
	public static String URL_LOGIN="http://10.57.116.26:8888/accounts/login/";
	public static String USER="woakas";
	public static String PASSWORD="asdfasdf";
	
	public ConnectHttp(){
		cookie="";
		
	}
	
	public URLConnection getUrl(String url){ 
		URL ur;
		try {
			
			//Trata de entrar a la url solicitada 
			ur = new URL(url);
			HttpURLConnection connection = (HttpURLConnection )ur.openConnection();
			connection.setRequestProperty("Cookie",cookie);
			connection.connect();
			
			// si la respuesta es 401 que significa que es unauthorized trata de entrar a la URL de login 

			if (connection.getResponseCode()==HttpURLConnection.HTTP_UNAUTHORIZED){
				ur = new URL(URL_LOGIN);
				connection = (HttpURLConnection )ur.openConnection();
				connection.setRequestMethod("POST");
				connection.setInstanceFollowRedirects(false);
				connection.setDoOutput(true);
				OutputStreamWriter output = new OutputStreamWriter(connection.getOutputStream());
				output.write("username="+USER+"&password="+PASSWORD);
				output.flush();
				
				//Toma la cookie y la setea
				String cook=connection.getHeaderField("set-cookie");
				cookie = cook.substring(0, cook.indexOf(";"));

				//Vuelve a tratar de entrar a la URL solicitada
				ur = new URL(url);
				connection = (HttpURLConnection )ur.openConnection();
				connection.setRequestProperty("Cookie",cookie);
				connection.connect();
				
				System.out.println(connection.getHeaderFields());

			}
			return connection;
		} 
		catch (MalformedURLException e) {} 
		catch (IOException e) {}
		return null;
				
	}
	
	 
	
	public static void main(String[] args) {
		
		ConnectHttp ch=new ConnectHttp();
		ch.getUrl("http://10.57.116.26:8888/mobile/login");
		ch.getUrl("http://10.57.116.26:8888/mobile/login");
	}

}
