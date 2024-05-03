package com.MobPriceCls.EndPoints.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import com.MobPriceCls.EndPoints.Repository.DeviceRepository;
import com.MobPriceCls.EndPoints.DTO.DeviceDTO;
import com.MobPriceCls.EndPoints.Utils.AppUtils;


@Service
public class DeviceService {
    @Autowired
    private DeviceRepository repository;

    public Flux<DeviceDTO> getDevices(){
        return repository.findAll().map(AppUtils::entityToDTO);
    }

    public Mono<DeviceDTO> getDevice(String id){
        return repository.findById(id).map(AppUtils::entityToDTO);
    }

    public Mono<DeviceDTO> saveDevice(Mono<DeviceDTO> DeviceDTOMono){
        return  DeviceDTOMono.map(AppUtils::DTOToEntity)
                .flatMap(repository::insert)
                .map(AppUtils::entityToDTO);
    }

    public Mono<DeviceDTO> updateDevice(Mono<DeviceDTO> DeviceDTOMono, String id){
        return repository.findById(id)
                .flatMap(p->DeviceDTOMono.map(AppUtils::DTOToEntity)
                        .doOnNext(e->e.setId(id)))
                .flatMap(repository::save)
                .map(AppUtils::entityToDTO);

    }

    public Mono<Void> deleteDevice(String id){
        return repository.deleteById(id);
    }
}
