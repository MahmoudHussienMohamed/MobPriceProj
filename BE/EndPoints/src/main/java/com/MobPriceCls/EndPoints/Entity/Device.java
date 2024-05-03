package com.MobPriceCls.EndPoints.Entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Document(collection = "devices")
public class Device {
    @Id
    private String id;
    private int battery_power;
    private int blue;
    private float clock_speed;
    private int dual_sim;
    private float fc;
    private float four_g;
    private float int_memory;
    private float m_dep;
    private float mobile_wt;
    private float n_cores;
    private float pc;
    private float px_height;
    private float px_width;
    private float ram;
    private float sc_h;
    private float sc_w;
    private int talk_time;
    private int three_g;
    private int touch_screen;
    private int wifi;
    private Integer price_range;
}
