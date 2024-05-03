package com.MobPriceCls.EndPoints.Repository;

import com.MobPriceCls.EndPoints.Entity.Device;
import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DeviceRepository extends ReactiveMongoRepository<Device, String> {
}
