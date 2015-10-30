package selenide;

import SOAP.SoapAction;
import com.codeborne.selenide.SelenideElement;
import org.junit.Test;
import org.openqa.selenium.By;

import static com.codeborne.selenide.Condition.visible;
import static com.codeborne.selenide.Selenide.*;

public class Login {

   // @BeforeClass
    public static void Initial() {
        open("http://rt-oss-mgmt-1.ds.local:8380/oms-gui/index.html");
        $(By.name("j_username")).val("admin");
        $(By.name("j_password")).val("admin").submit();
    }

    public void passwordEmpty() {
        $(By.name("j_username")).val("admin");
        $(By.name("j_password")).val("").submit();
    }

    public void nameEmpty() {
        $(By.name("j_username")).val("");
        $(By.name("j_password")).val("").submit();
    }

    public void loginTrue() {
        $(By.name("j_username")).val("admin");
        $(By.name("j_password")).val("admin").submit();
    }

    //@Test
    public void login() {
        open("http://rt-oss-mgmt-1.ds.local:8380/oms-gui/index.html");
        passwordEmpty();
        $(".zmdi-arrow-back").click();
        nameEmpty();
        $(".zmdi-arrow-back").click();
        loginTrue();
        //open("http://rt-oss-mgmt-1.ds.local:8380/oms-gui/index.html#/dashboard");
        $(".zmdi-search").click();
        for (SelenideElement selenideElement : $$("h2")) {
            if (selenideElement.is(visible)) {
                System.out.println(selenideElement.getText());
            }
        }
    }

    @Test
    public void iptv_pr() throws Exception {
        //System.out.println("Test0");
        SoapAction.request("LYRA", "iptv_access");
        //System.out.println("Test");
    }

    @Test
    public void voip_pr() throws Exception {
       // System.out.println("Test0");
        SoapAction.request("LYRA", "voip_access");
        //System.out.println("Test");
    }
}
