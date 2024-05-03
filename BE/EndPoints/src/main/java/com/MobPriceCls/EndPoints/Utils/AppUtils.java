package com.MobPriceCls.EndPoints.Utils;

import com.MobPriceCls.EndPoints.Entity.Device;
import com.MobPriceCls.EndPoints.DTO.DeviceDTO;
import org.springframework.beans.BeanUtils;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import reactor.core.publisher.Mono;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;


public class AppUtils {
    private static Map<String, Object> deviceDTOToMap(DeviceDTO deviceDTO) {
        Map<String, Object> map = new HashMap<>();
        Field[] fields = DeviceDTO.class.getDeclaredFields();
        for (Field field : fields) {
            if (field.getName().equals("id") || field.getName().equals("price_range")) {
                continue;
            }
            field.setAccessible(true);
            try {
                Object value = field.get(deviceDTO);
                map.put(field.getName(), value);
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            }
        }

        return map;
    }
    public static Mono<DeviceDTO> predictPriceRange(Mono<DeviceDTO> deviceMono) {
        String URL = "http://localhost:5000/predict_price_range";

        return deviceMono.flatMap(deviceDTO -> {
            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, Object> requestBody = deviceDTOToMap(deviceDTO);
            HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(requestBody, headers);
            Integer priceRange = null;

            ResponseEntity<Map> responseEntity = restTemplate.postForEntity(URL, requestEntity, Map.class);
            if (responseEntity.getStatusCode() == HttpStatus.OK) {
                Map<String, Object> responseBody = responseEntity.getBody();
                if (responseBody != null && responseBody.containsKey("price_range")) {
                    priceRange = (Integer) responseBody.get("price_range");
                    deviceDTO.setPrice_range(priceRange);
                }
            }
            deviceDTO.setPrice_range(priceRange);
            return Mono.just(deviceDTO);
        });
    }

    public static DeviceDTO entityToDTO(Device device){
        DeviceDTO deviceDTO = new DeviceDTO();
        BeanUtils.copyProperties(device, deviceDTO);
        return deviceDTO;
    }
    public static Device DTOToEntity(DeviceDTO deviceDTO){
        Device device = new Device();
        BeanUtils.copyProperties(deviceDTO, device);
        return device;
    }
}
