package SOAP;

import javax.xml.soap.*;
import java.io.*;

import static java.lang.Thread.sleep;


public class SoapAction {

    public static void response(String comand, String cfs, int orderId, int timeSleep) throws Exception {
        sleep(timeSleep);
        Runtime.getRuntime().exec("python send_responses.py " + orderId + " " + comand + " " + cfs);
    }

    public static int request(String cfs) {
        int orderId = -1;
        try {
            Process p = Runtime.getRuntime().exec("python send_request.py " + "_ " + cfs);

            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String rez = in.readLine();
            orderId = Integer.parseInt(rez.substring(34, 39));
        }
        catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return orderId;
    }
}

