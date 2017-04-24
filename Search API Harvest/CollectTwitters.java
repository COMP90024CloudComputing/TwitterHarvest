import java.util.ArrayList;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;
import org.lightcouch.CouchDbClient;
import org.lightcouch.CouchDbException;
import org.lightcouch.CouchDbProperties;
import org.lightcouch.DocumentConflictException;
import twitter4j.*;
import twitter4j.conf.ConfigurationBuilder;

import java.io.PrintStream;

/**
 * Created by HOU ZHENQIAN on 15/04/2017.
 * ID:720261
 * @UNIMELB
 */

public class CollectTwitters {
    private List<Twitter> twitter = new ArrayList<Twitter>();
    private Twitter currentFo;
    private Twitter currentTw;
    private CouchDbClient DbClient;
    private Date timelim = new Date(117, 3, 18);
    private List<Long> followerIDs = new LinkedList<Long>();
    final int max = 5000;
    private int count = 0;
    private List<Long> checkedFollowerIDs = new ArrayList<Long>();
    private long checked = 0;
    private long stID = 1;
    String command = "";
    Boolean f = false;

    private void initdeveloper() {


        initkey("okLGrJ9I95zk5KLktA5qfQ3cg","LlFl8o3XQEbN1uE3pmJdhgaTPIhDshKFHca1SCvz2cBXlycKOt");
        initkey("GSIfPUohau57i98QXgsxjbVCN","lvfGh9w4t7WjmQjXkN8oDQiS8aHB2FMffgniZfcDNxRxrDuf9Z");
        initkey("I19z51HfJDD05o2wIhTOFvpzB","mSt8AafM7LVUXlvyrR5aUJoe4M8igCpIEnfQmcrMibXLxqUFhl");
        initkey("H3n3d7z0RVzFIVp2d1Uiog8RF","hVdSqbFXtzHpozC05SmnuVHgpFyIGhVoIEMAh6PunyaERf1NeT");
        initkey("sJJbn4uZazMUd18cLfIYSGgDb","Cz99UtkmPZXiwrtSKs7JwEOnpx0lyj8itxlLB5Rqveq0urTu5u");
        initkey("jEPJlFINMxT0iGRc8syNYZjbo","0RLFLnFtB6TkxFNM5lTEb5o1ilmnANqEa9T7MQAhOhCCpuc3NW");
        initkey("D5m0tLIjJINfwBuqFM7nYkqhH","VJrvvZkEz8dSVBxZKxLU0dVrHLkg2ocZevUnQ9qr8p4OadKhZ7");
        initkey("WJpexHyqYFXL1vGWyJ0CxDswN","KyTJAfXO0tIz9V61fedlBWjPkEXFi5uNMSkUAkRE9k5LDhGePH");
        initkey("IYPLk5R7zNReYS3oC1mXmjbbT","RS6w3obOu1haswRTYF7AhbuACZKcad95iuYF2cbo4spAbkUMZe");
        initkey("ALmRd4i7pRPK4OrmQRSwqNcrD","UtcWKXEBGlpiMN5xACdN2QtR6nQz49gomeBPej9JlqUgjqqwhM");

        currentFo = twitter.get(0);
        currentTw = twitter.get(0);
    }

    private void initkey(String key, String secret) {
        ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setApplicationOnlyAuthEnabled(true);
        cb.setDebugEnabled(true);
        cb.setOAuthConsumerKey(key);
        cb.setOAuthConsumerSecret(secret);
        Twitter twitterGrab = new TwitterFactory(cb.build()).getInstance();
        try {
            twitterGrab.getOAuth2Token();
        } catch (TwitterException te) {
            System.out.println("[ERROR IN KEY :]" + key);
            System.out.println(te.getMessage());
        }
        twitter.add(twitterGrab);
    }

    private void changeFo() {
        int currentFollowersAccountIndex = twitter.indexOf(currentFo);
        currentFollowersAccountIndex = (currentFollowersAccountIndex +1)%20;
        currentFo = twitter.get(currentFollowersAccountIndex);
        System.out.println("Current Account NO." + currentFollowersAccountIndex);
        try {
            if (currentFo.getRateLimitStatus().get("/followers/ids").getRemaining() < 8) {
                do {
                    f = false;
                    Thread.sleep(180000);
                    break;
                } while (currentFo.getRateLimitStatus().get("followers/ids").getRemaining() < 8);

            }else {
                f =true;
            }
        } catch (TwitterException te) {
            System.out.println("[ERROR] IN Changing Follower Account");
        } catch (IllegalStateException e) {
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        if (f) {
            System.out.println("Change Follower Account complete!");
        }
    }

    private void changeTw()  {
        int currentTwitterAccountIndex = twitter.indexOf(currentTw);
        currentTwitterAccountIndex = (currentTwitterAccountIndex +1)%20;
        currentTw = twitter.get(currentTwitterAccountIndex);
        System.out.println("Try to change account to NO." + currentTwitterAccountIndex);
        try {
            if (currentTw.getRateLimitStatus().get("/statuses/user_timeline").getRemaining() < 40) {
                for (int i = 0; currentTw.getRateLimitStatus().get("/statuses/user_timeline").getRemaining() < 40; i ++){
                    if (i > 0) {
                        System.out.println("[ERROR] in current account [busy] --- skip to next one.  NO." + (currentTwitterAccountIndex + 1));
                        changeTw();
                        return;
                    }
                    try {
                        System.out.println("Wait 5 secs");
                        Thread.sleep(5000);
                    } catch (InterruptedException ie) {
                    }
                }
            }
        } catch (Exception e) {
            System.out.println("Exception happened when changing Twitter account!!! " +  e.getMessage());
        }
        System.out.println("Change Account successfully!");
    }

    private void getTw(long Id, Date sttime) {
        System.out.println("current solved twitter: " + Id);
        Paging paging = new Paging();
        paging.setCount(5000);
        paging.setSinceId(stID);
        paging.setMaxId(Long.MAX_VALUE - 1);
        boolean afterSinceTime = true;
        while (afterSinceTime) {
            try {
                ResponseList<Status> statuses = currentTw.getUserTimeline(Id, paging);
                if (statuses.isEmpty()) {
                    System.out.println(Id +"'s all twitter has been solved");
                    break;
                }
                checked += statuses.size();
                for (Status status : statuses) {
                    if (status.getId() < paging.getMaxId()) {
                        paging.setMaxId(status.getId() - 1);
                    }
                    if (status.getCreatedAt().before(sttime)) {
                        if (status.getId() > stID) {
                            stID = status.getId();
                        }
                        afterSinceTime = false;
                        System.out.println("[ALARM] IN pass time ---- give up current TW" + status.getCreatedAt());
                        break;
                    }
                    //if (status.getGeoLocation() != null ) {
                      //  AusGeoLocation geoLocation = new AusGeoLocation(status.getGeoLocation().getLatitude(), status.getGeoLocation().getLongitude());
                       // if (geoLocation.isAusArea()) {
                            count += 1;
                            System.out.println(count);
                            updateDB(status);
                       // }
                    //}
                }
            } catch (TwitterException te) {
                if (te.exceededRateLimitation()) {
                    changeTw();
                    continue;
                } else if (te.getStatusCode() == 401) {
                    System.out.println("[ERROR] IN current account[protected]");
                    break;
                } else {
                    System.out.println("[ERROR]  unknown");
                    System.out.println(te.getMessage());
                }
            }
        }
        checkedFollowerIDs.add(new Long(Id));
    }

    private void getFo(long Id) {
        long cursor = -1;
        IDs iDsResult;
        while (followerIDs.size() < 2000){
            try {
                iDsResult = currentFo.getFollowersIDs(Id, cursor, max);
                cursor = iDsResult.getNextCursor();
                long[] ids_long = iDsResult.getIDs();
                int len = ids_long.length;
                for (int i = 0; i < len; i ++) {
                    Long id_long = new Long(ids_long[i]);
                    if ((!followerIDs.contains(id_long))&&(!checkedFollowerIDs.contains(id_long))){
                        followerIDs.add(new Long(ids_long[i]));
                    }
                }
                System.out.println("Number of followers: " + followerIDs.size());
                if (!iDsResult.hasNext()) {
                    break;
                }
            } catch (TwitterException te) {
                if (te.exceededRateLimitation()) {
                    changeFo();
                    continue;
                }
            }
        }
    }

    private void initDB() {
        CouchDbProperties properties = new CouchDbProperties()
                .setDbName("twitter_foll")
                .setCreateDbIfNotExist(true)
                .setProtocol("http")
                .setHost("115.146.93.233")
                .setPort(5984);
        DbClient = new CouchDbClient(properties);
    }

    private void initDB(String DBname, String IP) {
        CouchDbProperties properties = new CouchDbProperties()
                .setDbName(DBname)
                .setCreateDbIfNotExist(true)
                .setProtocol("http")
                .setHost(IP)
                .setPort(5984);
        DbClient = new CouchDbClient(properties);
        System.out.println("Database Check...         ***STANDBY***");
    }

    private void updateDB(Status status) {
        try {
            DbClient.save(new TwitterElement(status));
            System.out.println("UPDATED");
        } catch (DocumentConflictException dce) {
            System.out.println("Repetitive Tw: " + status.getId());
        } catch (CouchDbException e) {
            System.out.println(e.getMessage());
        }
    }

    public void collect(String[] args) {
        if (args.length == 0) {
            initDB();
        } else {
            if (args.length == 2) {
                initDB(args[0], args[1]);
            }else {
                System.out.println("Wrong Input !");
            }
        }
        initdeveloper();
        System.out.println("Developer ACC Check...    ***STANDBY***");
        while (!command.equals("exit")) {
            getFo(19050000);
            System.out.println(followerIDs.size());
            getTw(19050000, timelim);
            System.out.println("Target ACC Check...       ***STANDBY***");
        while (!followerIDs.isEmpty()) {
            long id = followerIDs.remove(0);
            if (followerIDs.size() < 2000) {
                getFo(id);
            }
            getTw(id,timelim);
            System.out.println("Already checked " + checked + " tweets from " + checkedFollowerIDs.size() + " IDs");
        }
            long current =System.currentTimeMillis();
            current -=30*60*1000;
            timelim = new Date(current);
            System.out.println("***********next round**********");
        }
    }

    public static void main(String[] args) {

        new CollectTwitters().collect(args);
    }
}
