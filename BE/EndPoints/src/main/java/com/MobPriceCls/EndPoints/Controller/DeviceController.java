package com.MobPriceCls.EndPoints.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import com.MobPriceCls.EndPoints.DTO.DeviceDTO;
import com.MobPriceCls.EndPoints.Service.DeviceService;
import com.MobPriceCls.EndPoints.Utils.AppUtils;

@RestController
@RequestMapping("/MobPriceCls/api")
public class DeviceController {

    @Autowired
    private DeviceService service;

    @GetMapping("/devices")
    public Flux<DeviceDTO> getDevices(){
        return service.getDevices();
    }

    @GetMapping("/devices/{id}")
    public Mono<DeviceDTO> getDevice(@PathVariable String id){
        return service.getDevice(id);
    }

    @PostMapping("/devices")
    public Mono<DeviceDTO> saveDevice(@RequestBody Mono<DeviceDTO> DeviceDTOMono){
        return service.saveDevice(DeviceDTOMono);
    }

    @PostMapping("/predict/{deviceId}")
    public Mono<DeviceDTO> predictDevice(@PathVariable String deviceId) {
        return service.getDevice(deviceId)
                .flatMap(deviceDTO -> {
                    Mono<DeviceDTO> updatedDeviceMono = AppUtils.predictPriceRange(Mono.just(deviceDTO));
                    return service.updateDevice(updatedDeviceMono, deviceId);
                });
    }

}