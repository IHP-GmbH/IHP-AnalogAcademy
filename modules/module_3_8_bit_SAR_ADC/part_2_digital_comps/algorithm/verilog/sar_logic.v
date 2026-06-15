module sar_logic (
    input wire clk,
    input wire Op,
    input wire En,
    input wire Om,
    input wire rst,
    output wire [7:0] B,  // 8-bit
    output reg [7:0] BN,  // 8-bit
    output reg [7:0] D    // 8-bit
);

  reg [3:0] counter; // 3-bit counter
  assign B = D;

  always @(posedge clk) begin
    if (rst) begin
      BN <= 8'b0000000;
      D <= 8'b00000000;
      counter <= 4'b0000;
    end else if (En && (Op ^ Om) && ~(counter==8)) begin
      D[counter[2:0]] <= Op;
      BN[counter[2:0]] <= Om;
      counter <= counter + 1'b1;
    end
  end
endmodule
