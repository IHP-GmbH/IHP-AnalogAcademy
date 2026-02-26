`timescale 1ns/1ps

module sar_logic_tb();

    // Inputs
    reg clk;
    reg rst;
    reg Op;
    reg Om;
    reg En;

    // Outputs
    wire [7:0] B;
    wire [7:0] BN;
    wire [7:0] D;

    // Instantiate the SAR Logic module
    sar_logic uut (
        .clk(clk),
        .rst(rst),
        .Op(Op),
        .Om(Om),
        .En(En),
        .B(B),
        .BN(BN),
        .D(D)
    );

    // Clock generation
    always #5 clk = ~clk;

    // Test sequence
    initial begin
        $dumpfile("sar_logic_tb.vcd");  // Name of the VCD file
        $dumpvars(0, sar_logic_tb);     // Dump all variables in the testbench

        // Initialize inputs
        clk = 1'b0;
        rst = 1'b1;
        Op = 1'b0;
        Om = 1'b0;
        En = 1'b0;

        // Apply reset
        #20 rst = 1'b0;
        En = 1'b1;
        Op = 1'b1;
        Om = 1'b0;

        // Apply reset again
        #100 rst = 1'b1;
        #10 rst = 1'b0;
        Op = 1'b0;
        Om = 1'b1;

        #50 rst = 1'b1;
	#10 rst = 1'b0;
        En = 1'b1;
        Op = 1'b1;
        Om = 1'b0;

        #10 Op = 1'b0;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;


        #50 rst = 1'b1;
	#10 rst = 1'b0;
        En = 1'b1;
	Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

	#10 Op = 1'b1;
        Om = 1'b0;

	#10 Op = 1'b0;
        Om = 1'b1;

        // End of simulation
        #100 $finish;
    end

endmodule

