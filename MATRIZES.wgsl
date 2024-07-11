@group(0) @binding(0)   // param_flt32
var<storage,read_write> matriz: array<f32>;

// function to convert 2D [j,n] index into 1D index
fn idx(n: i32, j: i32) -> i32 {{
    let n_sz: i32 = wsx;
    let j_sz: i32 = wsy;
    let index = i32(j + n*j_sz);

    return select(-1, index, j >= 0 && j < j_sz && n >= 0 && n < n_sz);
}}

@compute
@workgroup_size(wsx, wsy)
fn matriz_kernel(@builtin(global_invocation_id) index: vec3<u32>){

}