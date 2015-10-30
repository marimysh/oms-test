package SOAP;

import javax.xml.soap.*;
import java.io.*;

import static java.lang.Thread.sleep;


public class SoapAction {

    public static void request(String system, String cfs) throws Exception {
        try {
        /*ProcessBuilder pb = new ProcessBuilder("python",
                "C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\send_request.py", "_",
                "C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\requests\\" +
                        cfs + ".xml" );
        Process p = pb.start();*/

            Process p = Runtime.getRuntime().exec(//"cd " +
                    //"C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\ && " +
                    "python send_request.py "
                    + "_ " + cfs);

            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String rez = in.readLine();
            int orderid = Integer.parseInt(rez.substring(34, 39));
            //if (orderid != null) {
            System.out.println("Res P: " + orderid);
            sleep(2000);
            Runtime.getRuntime().exec("python send_responses.py " + orderid + " HVS");
            sleep(2000);
            Runtime.getRuntime().exec("python send_responses.py " + orderid + " HAS");
            sleep(2000);
            Runtime.getRuntime().exec("python send_responses.py " + orderid + " LCS");
            sleep(2000);
            Runtime.getRuntime().exec("python send_responses.py " + orderid + " WFS");
            sleep(2000);
            Runtime.getRuntime().exec("python send_responses.py " + orderid + " LOS");
            sleep(2000);
            Runtime.getRuntime().exec("python send_responses.py " + orderid + " HCS");
            //}
        }
        catch (Exception e) {
            System.out.println(e.getMessage());
        }
        /*
        // Create SOAP Connection
        String pathSystem = "";
        if (system.equals("LYRA"))
            pathSystem = "/lyra-adapter/LyraOmsService";
        else if (system.equals("WFM"))
            pathSystem = "/wfm-adapter/WfmToLiraApiService";
        else if (system.equals("SPA"))
            pathSystem = "/hpsa-adapter/ActivatorCallbackService";

        SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
        SOAPConnection soapConnection = soapConnectionFactory.createConnection();

        String url = "http://rt-sa-app-2.ds.local:8180" + pathSystem;
        SOAPMessage soapResponse = soapConnection.call(createSOAPRequest(cfs), url);

        // print SOAP Response
        System.out.println("Response SOAP Message:");
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        //soapResponse.writeTo(out);

        SOAPPart sp = soapResponse.getSOAPPart();
        SOAPEnvelope se = sp.getEnvelope();
        SOAPBody sb = se.getBody();

//        Iterator it = sb.getChildElements(bodyName);
  //      SOAPBodyElement bodyElement =
  //              (SOAPBodyElement)it.next();
  //      String lastPrice = bodyElement.getValue();*/
        //System.out.print(soapResponse.getSOAPBody().hasAttribute("OrderId"));
    }

    private static SOAPMessage createSOAPRequest(String cfs) throws Exception {
        File input = new File("C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\requests\\" +
                cfs + ".xml");
        InputStream is = new BufferedInputStream(new FileInputStream(input));
        SOAPMessage soapMessage = MessageFactory.newInstance().createMessage(null, is);
        /* Print the request message */
        //PrintStream out = new PrintStream(System.out, true, "UTF-8");
        //System.out.print("Request SOAP Message:");
        //soapMessage.writeTo(out);
        //System.out.println();
/*
        ProcessBuilder pb = new ProcessBuilder("python",
                "C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\send_request.py", "_",
                "C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\requests\\" +
                cfs + ".xml" );
        Process p = pb.start();
*/

        Process p = Runtime.getRuntime().exec("python " +
                "C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\send_request.py " + "_ " +
                "C:\\Users\\Temur\\Desktop\\rt-oms-lyra\\scripts\\oms-responses\\requests\\" +
                        cfs + ".xml");

        BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String rez = new String (in.readLine().toString());
        System.out.println("Res P: " + rez);
        return soapMessage;
    }
}

