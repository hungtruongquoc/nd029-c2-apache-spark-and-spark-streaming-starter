import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

/**
 * This class configures the ObjectMapper to disable FAIL_ON_EMPTY_BEANS
 * It will be loaded by the JVM before the Redis Source Connector
 */
public class ObjectMapperConfig {
    static {
        // Configure all ObjectMapper instances to disable FAIL_ON_EMPTY_BEANS
        System.setProperty("com.fasterxml.jackson.databind.SerializationFeature.FAIL_ON_EMPTY_BEANS", "false");
        
        try {
            // Get the default ObjectMapper and configure it
            ObjectMapper mapper = new ObjectMapper();
            mapper.disable(SerializationFeature.FAIL_ON_EMPTY_BEANS);
            
            System.out.println("ObjectMapperConfig: Configured ObjectMapper to disable FAIL_ON_EMPTY_BEANS");
        } catch (Exception e) {
            System.err.println("ObjectMapperConfig: Error configuring ObjectMapper: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
