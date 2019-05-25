package call_model;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class j2Py {

    public static void main(String[] args) {
        String filePath = "D:\\Project\\NCSISI\\asv\\NCSISC\\ASR\\GMM-UBM\\VoicePrintR.py";

        //String[] cmd_enroll = new String[]{"python", filePath, "enroll", "zky"};
        String[] cmd_login = new String[]{"python", filePath, "login", "zky", "zky_test_1"};
        call(cmd_login);
    }

    /**
     * 用户声纹注册
     * {"python","../enroll.py","username"}
     * <p>
     * 用户登录
     * {"python", "../login.py", "username", "file path"}
     *
     * @param cmds python脚本执行参数
     */
    public static String call(String[] cmds) {
        String result = "";
        try {
            Process pr = Runtime.getRuntime().exec(cmds);
            pr.waitFor();
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
            String line = null;

            while ((line = in.readLine()) != null) {
                result += line + "\n";
            }
            in.close();
            int r = pr.waitFor();
            System.out.println(r);
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println(result);
        return result;

    }

}

