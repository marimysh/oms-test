package selenide;

import SOAP.SoapAction;
import org.junit.Test;


public class RequestCfs {
    @Test
    public void iptv_pr() throws Exception {
        String cfs = "iptv_access";
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs, orderId, 2000);
        SoapAction.response("HAS", cfs, orderId, 1000);
        SoapAction.response("LCS", cfs, orderId, 2000);
        SoapAction.response("WFS", cfs, orderId, 2000);
        SoapAction.response("LOS", cfs, orderId, 2000);
        SoapAction.response("HCS", cfs, orderId, 2000);
    }

    @Test
    public void voip_pr() throws Exception {
        String cfs = "voip_access";
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs, orderId, 2000);
        SoapAction.response("HAS", cfs, orderId, 1000);
        SoapAction.response("LCS", cfs, orderId, 2000);
        SoapAction.response("WFS", cfs, orderId, 2000);
        SoapAction.response("LOS", cfs, orderId, 2000);
        SoapAction.response("HCS", cfs, orderId, 2000);
    }

    @Test
    public void pmi_1() throws Exception {
        String cfs_line = "line_provision_lyra",
                cfs_internet = "internet_access_lyra",
                cfs_fix_ip = "fixed_ip_lyra",
                cfs_parent = "parent_control_lyra",
                cfs_torrent = "torrent_lyra";
        String cfs = cfs_line + " " + cfs_internet + " " + cfs_fix_ip + " " + cfs_parent + " " + cfs_torrent;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_line, orderId, 2000);
        SoapAction.response("HAS", cfs_line, orderId, 1000);
        SoapAction.response("HVS", cfs_internet, orderId, 2000);
        SoapAction.response("HAS", cfs_internet, orderId, 1000);
        SoapAction.response("HVS", cfs_fix_ip, orderId, 2000);
        SoapAction.response("HAS", cfs_fix_ip, orderId, 1000);
        SoapAction.response("LCS", cfs_line, orderId, 2000);
        SoapAction.response("LCS", cfs_internet, orderId, 2000);
        SoapAction.response("WFS", "", orderId, 2000);
        SoapAction.response("LOS", cfs_line, orderId, 2000);
        SoapAction.response("LOS", cfs_internet, orderId, 2000);
        SoapAction.response("HVS", cfs_parent + " " + cfs_torrent, orderId, 2000);
        SoapAction.response("HAS", cfs_parent + " " + cfs_torrent, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_2() throws Exception {
        String cfs_fix_ip = "fixed_ip_CE_lyra",
                cfs_parent = "parent_control_CE_lyra",
                cfs_torrent = "torrent_CE_lyra";
        String cfs = cfs_fix_ip + " " + cfs_parent + " " + cfs_torrent;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_fix_ip, orderId, 2000);
        SoapAction.response("HAS", cfs_fix_ip, orderId, 1000);
        SoapAction.response("HVS", cfs_parent + " " + cfs_torrent, orderId, 2000);
        SoapAction.response("HAS", cfs_parent + " " + cfs_torrent, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_3() throws Exception {
        String cfs_pay_on_credit = "pay_on_credit_lyra",
                cfs_content = "pump_up_content_lyra",
                cfs_surfing = "surfing_lyra";
        String cfs = cfs_pay_on_credit + " " + cfs_content + " " + cfs_surfing;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_content, orderId, 2000);
        SoapAction.response("HAS", cfs_content, orderId, 1000);
        SoapAction.response("HVS", cfs_surfing, orderId, 2000);
        SoapAction.response("HAS", cfs_surfing, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_4() throws Exception {
        String cfs_pay_on_credit = "pay_on_credit_CE_lyra",
                cfs_content = "pump_up_content_CE_lyra",
                cfs_surfing = "surfing_CE_lyra";
        String cfs = cfs_pay_on_credit + " " + cfs_content + " " + cfs_surfing;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_content, orderId, 2000);
        SoapAction.response("HAS", cfs_content, orderId, 1000);
        SoapAction.response("HVS", cfs_surfing, orderId, 2000);
        SoapAction.response("HAS", cfs_surfing, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_5() throws Exception {
        String cfs_speed = "speed_lyra",
                cfs_cancel_restrictions = "cancel_restrictions_lyra",
                cfs_safe_internet = "safe_internet_lyra";
        String cfs = cfs_speed + " " + cfs_cancel_restrictions + " " + cfs_safe_internet;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_speed, orderId, 2000);
        SoapAction.response("HAS", cfs_speed, orderId, 1000);
        SoapAction.response("HVS", cfs_cancel_restrictions, orderId, 2000);
        SoapAction.response("HAS", cfs_cancel_restrictions, orderId, 1000);
        SoapAction.response("HVS", cfs_safe_internet, orderId, 2000);
        SoapAction.response("HAS", cfs_safe_internet, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_6() throws Exception {
        String cfs_speed = "speed_CE_lyra",
                cfs_cancel_restrictions = "cancel_restrictions_CE_lyra",
                cfs_safe_internet = "safe_internet_CE_lyra";
        String cfs = cfs_speed + " " + cfs_cancel_restrictions + " " + cfs_safe_internet;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_speed, orderId, 2000);
        SoapAction.response("HAS", cfs_speed, orderId, 1000);
        SoapAction.response("HVS", cfs_cancel_restrictions, orderId, 2000);
        SoapAction.response("HAS", cfs_cancel_restrictions, orderId, 1000);
        SoapAction.response("HVS", cfs_safe_internet, orderId, 2000);
        SoapAction.response("HAS", cfs_safe_internet, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_7() throws Exception {
        String cfs_social = "social_network_lyra";
        String cfs = cfs_social;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_social, orderId, 2000);
        SoapAction.response("HAS", cfs_social, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_8() throws Exception {
        String cfs_social = "social_network_CE_lyra";
        String cfs = cfs_social;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_social, orderId, 2000);
        SoapAction.response("HAS", cfs_social, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_9() throws Exception {
        String cfs_half_price = "half_price_lyra";
        String cfs = cfs_half_price;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_half_price, orderId, 2000);
        SoapAction.response("HAS", cfs_half_price, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_10() throws Exception {
        String cfs_half_price = "half_price_CE_lyra";
        String cfs = cfs_half_price;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_half_price, orderId, 2000);
        SoapAction.response("HAS", cfs_half_price, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_11() throws Exception {
        String cfs_day_night = "day_night_lyra";
        String cfs = cfs_day_night;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_day_night, orderId, 2000);
        SoapAction.response("HAS", cfs_day_night, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_12() throws Exception {
        String cfs_suspend = "suspend_i_lyra";
        String cfs = cfs_suspend;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_suspend, orderId, 2000);
        SoapAction.response("HAS", cfs_suspend, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }

    @Test
    public void pmi_13() throws Exception {
        String cfs_suspend = "suspend_i_CE_lyra";
        String cfs = cfs_suspend;
        int orderId = SoapAction.request(cfs);
        SoapAction.response("HVS", cfs_suspend, orderId, 2000);
        SoapAction.response("HAS", cfs_suspend, orderId, 1000);
        SoapAction.response("HCS", "", orderId, 2000);
    }
}
